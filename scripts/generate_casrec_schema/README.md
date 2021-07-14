Sorry about the mess, but this should only really be needed as a one off, and I already did that so this is just here for posterity :)




This does 3 things:

1. run `generate_file_per_table.py` takes the `casrec_dd - main.csv` and turns it into one CSV per table.

    These files are then used by the following steps

1. run `create_tables.py` to create the casrec table definitions (as `CREATE` statements) in the file `create_tables.sql`

1. run `get_relationships.py` to generate the fk links between the casrec tables (as `ALTER` statements) in the file `create_tables.sql`, this appends to the file so if you've run it once you'll need to delete some stuff before you run it again


You can run this against the `casrec_db` database, it will create everything in a different schema (called `reference`) so it doesn't interfere with anything important.


Be aware, this is not definitive. We already know some of the datatypes are wrong and I'm missing some lookup tables so it's a gist, not a truth.
