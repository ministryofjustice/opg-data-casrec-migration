import logging
import sys

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def


# prepfn: function with signature
#     prepfn(db_config, target_db, mapping_file_name): dict
# run once for the whole migration. This builds any subsidiary selects etc.
# and produces a dict as output, which is passed to chunkfn.
#
# chunkfn: function with signature
#     chunkfn(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep=None): tuple
# run once per chunk. prep is the output of prepfn, which will be passed to each chunk.
# It should return (dataframe, more_records), where dataframe is a (possibly empty) dataframe and
# more_records is a boolean which is True if another chunk should be tried, False otherwise.
#
# sirius_details is also calculated once and passed to chunkfn for each chunk
def transformer(db_config, target_db, mapping_file, chunkfn, prepfn=None):
    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    prep = None
    if prepfn != None:
        prep = prepfn(db_config, target_db, mapping_file_name)

    more_records = True

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
            if df is not None and len(df) > 0:
                # this also creates the table if it doesn't exist, as a side effect
                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=df,
                    sirius_details=sirius_details,
                    chunk_no=chunk_no,
                )

                chunk_no += 1
                offset += chunk_size

            # first chunk and no records, so create the table now
            elif chunk_no == 1:
                target_db.create_empty_table(sirius_details=sirius_details, df=df)

        except EmptyDataFrame as e:
            # don't try any more chunks: chunkfn() threw an exception
            more_records = False

        except Exception as e:
            logging.getLogger('root').exception(e)
            sys.exit(1)