import logging
import sys

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def


log = logging.getLogger('root')

# chunkfn: function with signature
#     chunkfn(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep=None): tuple
# Runs once per chunk. prep is the output of prepfn, which will be passed to each chunk.
# chunkfn should return (dataframe, more_records), where dataframe is a (possibly empty) dataframe and
# more_records is a boolean which is True if another chunk should be tried, False otherwise.
#
# prepfn: function with signature
#     prepfn(db_config, target_db, mapping_file_name): dict
# Runs once for the whole migration. This builds any subsidiary selects etc.
# and produces a dict as output, which is passed to chunkfn.
#
# sirius_details is also calculated once and passed to chunkfn for each chunk
def transformer(db_config, target_db, mapping_file, chunkfn, prepfn=None):
    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1
    more_records = True
    records_inserted = 0

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)

    destination_table = table_definition["destination_table_name"]

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    prep = None
    if prepfn != None:
        prep = prepfn(db_config, target_db, mapping_file_name)

    while more_records:
        try:
            df, more_records = chunkfn(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_size=chunk_size,
                offset=offset,
                prep=prep,
            )

            # only insert dataframes with records, otherwise insert_data()
            # throws an EmptyDataFrame exception; we don't want this here,
            # as it might just be this chunk that's empty due to filtering,
            # and there are more viable records in the next chunk
            num_records = 0
            if df is not None:
                num_records = len(df)

            if num_records > 0:
                # this also creates the table if it doesn't exist, as a side effect
                target_db.insert_data(
                    table_name=destination_table,
                    df=df,
                    sirius_details=sirius_details,
                    chunk_no=chunk_no,
                )

                records_inserted += num_records

            # we've never inserted any records, and there are no more records available,
            # so create the table before we exit the loop; if there were
            # records, the insert_data() function will have created the table
            # (and records_inserted will be > 0);
            # if the original unfiltered dataframe had records (which were filtered out)
            # more_records will be True and we won't create the table here
            #
            # caveat: if we never find a chunk with records in it (e.g. the filter is wrong
            # or it's right but filters out all the records in dev), it's possible
            # that the dataframe will be incomplete, possibly missing columns,
            # have the wrong datatypes on columns etc., and that the table SQL will be
            # wrong, too
            elif not more_records and records_inserted == 0:
                target_db.create_empty_table(sirius_details=sirius_details, df=df)
                log.warning(f'NO RECORDS INSERTED INTO {destination_table}; CREATED TABLE MAY BE INVALID')

            chunk_no += 1
            offset += chunk_size

        except Exception as e:
            # this will catch any EmptyDataFrame exceptions which are not expected,
            # so make sure all _chunk/_records functions catch them or you'll end up here
            log.exception(e)
            sys.exit(1)

    log.info(f'Inserted {records_inserted} into {destination_table}')
