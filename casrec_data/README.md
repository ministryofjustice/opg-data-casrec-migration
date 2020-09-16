# How to run these scripts

Steps 1 and 2 are temporary and will no longer be relevant once we have suitable sample data.

Steps 3 and 4 are expected to only be run when building the containers, so these will need to be refactored accordingly.
Once we have suitable data to work with, the create/schema files will be fixed, we don't want to dynamically create
the DB from the CSV files.


1. #### Create fake sample data 

   ```bash
   cd create_test_data	
   python3 create_empty_files.py
   ```

   *We don't want the real sample data locally, but we need to check the anonymising works.*  
   *This will create a load of CSVs in the same format as the sample data, but with placeholder data* 

2. #### Run the anonymising on the fake sample data

   ```bash
   cd ../do_anonymising
   python3 anon_csv_data.py
   
   ```

   *Creates a folder of CSVs based off the sample data, but with personal data replaced with random values from Faker.* 

   *IRL, this would be run on Cloud9, and the resulting files would be downloaded manually. The real data would never 
   touch our local envs - this is just for testing the anonymising and db creation scripts.*  

3. #### Create the casrec database tables

   ```bash
   cd ../create_db
   cp -r ../do_anonymising/anon_data/ ../anon_data
   python3 create_casrec_db_tables.py
   cd ../..
   docker-compose up --build
   ```

   *The script dumps an sql file full of create statements based off the column headings of the CSV files with generic text datatypes. 
   The docker-compose uses when building the container*

4. #### Insert the anonymised test data 

   ######You will need the casrec postgres container running and the tables created to run this as it connects directly to the pg database
    
   ```bash
   cd ../create_db
   python3 insert_data.py
   ```

    *The `cp` is only because we're using the test data generated above. When we have the real anonymised data we won't 
    need to do this bit*
