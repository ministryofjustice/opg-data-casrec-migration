# Mapping Document

## Worksheets

The default is one per table, however you can add more if they are required.

For example, We are considering `clients` and `deputies` as two seperate entities, so it makes sense to split the `persons` transformations into two parts. In this case we can create an extra worksheet, so we have `persons_client` and `persons_deputy`. These both have the same Sirius details, but with different mapping info for the entities.

We can do this as much as we need, as long as each sheet has a unique name. You can also remove sheets if you want to but it doesn't matter to the mapping - if they are not populated with mapping info then they are not exported.

If something goes wrong with a sheet, we can recreate them using the little script in `docs/support_scripts/generate_mapping_doc`

## Worksheet format


|          | Column Name             | Populated By | Details                         |
| -------- | ----------------------- | ------------ | ------------------------------- |
| Sirius   | column_name             | Sirius db    | Do not amend                    |
| Sirius   | data_type               | Sirius db    | Do not amend                    |
| Sirius   | is_pk                   | Sirius db    | Do not amend                    |
| Sirius   | fk_children             | Sirius db    | Do not amend                    |
| Sirius   | fk_parents              | Sirius db    | Do not amend                    |
| Casrec   | casrec_table            |              | Must match table name exactly   |
| Casrec   | casrec_column_name      |              | Must match column name exactly* |
| Analysis | requires_transformation |              | Choose from list (see below)    |
| Analysis | calculated              |              | Choose from list (see below)    |
| Analysis | default_value           |              | If required                     |
| Analysis | is_complete             |              | Yes or No                       |
| Analysis | comments                |              |                                 |



### <u>Sirius Columns</u>

​	The first 5 rows will be generated directly from the Sirius database, please do not amend these.

### <u>Casrec Columns</u>

​	These will need to match the Casrec table and column names exactly. Case insensitve.

#### casrec_column_name - multiple columns

​	In the case that one column in Sirius is mapped to multiple columns in Casrec, then please do NOT duplicate the Sirius row, instead enter the `casrec_column_name` as a comma separated list, eg `Item1, Item2, Item3`

### <u>Analysis Columns</u>

​	These are to be filled in by the Migrations team.

#### requires_transformation

​	To be chosen from a list of standard transformations, current list is:

* `squash_columns`  converts a comma seperated list of columns into a single json array

* `convert_to_bool` casrec data is all stored as strings, this makes it into a proper boolean

* `unique_number` generates a unique 12 digit number

  These are just the basics at the moment, more will be added as we need them.

#### calculated

​	To be chosen from a list of available calculations, current list is:

* `current_date`  inserts the current date

  As above, these are just the basics at the moment, more will be added as we need them.

#### lookup_table

​	For lookup tables. Not sure how this works yet but we know we're going to need it.

#### default_value

​	If the column has a default value, this is the place to put it. Currently this is only applied when a casrec column is not mapped, so can't be used as a kind of backup of the casrec data is null.

#### is_complete

​	If we are totally happy with this mapping, set this to `Yes`. It will help keep track of what our unknowns are.

#### comments

​	For only your most insightful and interesting comments

#### etc etc etc...

​	Feel free to add more columns, but they will be for human reference only, and will not be used by the transformations.



## How to generate the json files for use in the ETL tasks

Assuming you have a venv up and running as per usual:

```bash
cd docs/support_scripts/mapping_doc_to_json
python3 app.py
```

You will be asked some questions, the answers are up to you. First, the location of the mapping spreadsheet, then, where would you like the files to end up - for ETL2 I use `.../../../migration_steps/transform_casrec/app/mapping_definitions`:

```python
path to the mapping spreadsheet [./docs/mapping_doc_mini.xlsx]:
path to the output directory [./json_files]:
```



