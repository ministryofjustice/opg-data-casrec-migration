# opg-data-casrec-migration

## Purpose

The purpose of this repo is to house all the code that we will use to perform the casrec to sirius migration.
Having investigated AWS Glue & pyspark, we are using pandas dataframes to transform the data set into a form that can then be
injested / inserted into Sirius platform.

We use AWS Localstack and postgres containers locally

## Setup from scratch


### Checkout

```bash
git clone git@github.com:ministryofjustice/opg-data-casrec-migration.git
```

All commands are from the root directory of `opg-data-casrec-migration` unless otherwise stated

### Set up python virtual environment

```bash
virtualenv venv
source venv/bin/activate

which python
> ...opg-data-casrec-migration/venv/bin/python
```

### Grab Casrec dev data

For development we have a sample set of migration data in the same format as the files we will be receiving from Casrec (about 40 files). Sensitive data has been removed - hence we call this our 'anonymised csv data'.

You need to save these files to `data/anon_data/` on your development machine

```bash
mkdir -p data/anon_data

# copy .csv files within this dir (about 40 files)
```

### Install python requirements

```bash
pip3 install -r base_image/requirements.txt
pip install pre-commit
```

## Run a local migration

### Docker setup
```bash
# do a prune first if you reading this having had problems with migrate.sh
docker-compose down
docker system prune -a
```

### Migrate

```bash
./migrate.sh
```

Or, you can run each step individually:

```bash
docker-compose run --rm load_s3 python3 load_s3_local.py
docker-compose run --rm prepare prepare/prepare.sh
docker-compose run --rm load_casrec python3 app.py
docker-compose run --rm transform_casrec python3 app.py --clear=True
docker-compose run --rm integration integration/integration.sh
docker-compose run --rm load_to_target python3 app.py
```

Running the steps (Non-dockerised):

Note - the steps rely on data passed forward by the chain, so your safest bet is to run ./migrate  - but for debugging.

Several of the steps you can increase the log debugging level with -vv, -vvv etc

```bash
python3 migration_steps/load_s3_local.py
./migration_steps/prepare/prepare.sh -vv
python3 migration_steps/load_casrec/app/app.py
python3 migration_steps/transform_casrec/app/app.py -vv
./migration_steps/integration/integration.sh -vv
python3 migration_steps/load_to_target/app/app.py
```

## Testing your work

### Run the tests

```bash
pip3 install pytest
pip3 install pytest_cases

# export test paths to PYTHONPATH with something like
export PYTHONPATH=[project root]/migration_steps/transform_casrec/tests:[project root]/migration_steps/transform_casrec/app:[project root]/migration_steps/transform_casrec

python3 -m pytest migration_steps/transform_casrec/tests
```

### Python linting - run precommit

Runs terraform_fmt, flake8, black etc

```bash
pre-commit run --all-files
```

## Other admin and utility scripts

### Importing latest spreadsheet and mapping definitions

Downloads the latest version of the file that is used to generate the mapping json docs.

Ensure you're in a virtual env that has the required dependencies and run:
- Requires AWS Vault - if you don't have that, somebody in Ops should be able to help out
- Assumes python requirements.txt installed as above

```bash
aws-vault exec identity -- python3 import_mapping_definitions.py
```

There are two flags:

- `s3_source` is to decide whether to pull from staged or merged (defaults to merged).
- `version` is to decide whether to pull in specific version (defaults to latest)

## Install Sirius project (optional)
In order to see the results of a migration in the Sirius Front end you'll need the actual Sirius project:

Installing Sirius in a nutshell (refer to Sirius docs for more):

```
git clone git@github.com:ministryofjustice/opg-sirius.git
cd opg-sirius

# authenticate with AWS (get ops to help you set this up if you haven't got aws-vault)
aws-vault exec sirius-dev-operator -- make ecr_login

make clean && make dev-setup
# (you can re-run make dev-setup if it fails, without doing a make-clean)
```

You should be able to view Sirius FE at http://localhost:8080
You should also be able to log in as case.manager@opgtest.com / Password1

If you can't log in, or if the site doesn't appear at all, but your containers seem to be up ok, It sometimes helps to turn it off and on again:

```
make dev-stop
make dev-up
```

You can now bring up our side using a different migrate script. You should bring everything down first. Run these commands in this repo:

```
docker-compose down
./migrate_to_sirius
```


Re-index elastic search after migration

```bash
# (In Sirius local dev root)
docker-compose run --rm queue scripts/elasticsearch/setup.sh
```

## The Migration Pipeline

Migrations are typically described as 'ETL' (Extract, Transform, Load) but we are building a series of smaller data transform steps, so it's more like ETTTT(...)L

The Migration steps, in order, are:

- load_s3
- prepare
- load_casrec
- transform_casrec
- integration
- load_to_target
- validation

### load_s3

- Runs in local dev only. Takes the anonymised dev data and loads it into an S3 bucket on localdev, so that the next step will find the files in S3 as it does in AWS proper

### prepare

- Runs some modifications on our local copy of sirius (dev only)
- Makes a copy of Sirius `api.public` schema called `pre_migration`. This will be used to hold our migration data before it is ready for loading, providing a final level of assurance that the data will 'fit' Sirius

### load_casrec

- Reads the S3 files and saves them intact into a postgres database schema, one table per csv file
- Schema created: `casrecmigration.etl1`

### transform_casrec

- Reads data from the `etl1` schema and performs a series of transformations on the columns
- Makes extensive use of pandas to perform the transformations
- Arrives at a schema more closely resembling the Sirius DB
- outputs schema `etl2`

### integration

- Copies `etl2` to `integration`, which has added id columns to hold associated ids from Sirius
- Generates ID lookup tables from the Sirius DB
- Uses the lookup tables to transpose the corresponding Sirius ids into the integration schema

### load_to_target

- takes the `pre_migrate` schema and performs a series of inserts where the data does not exist in Sirius, updates where it does.

### validation

- Validates data at the DB layer, by comparing Sirius `api.public` with `pre_migrate`
- Returns a list of expected vs actual counts
- Saves any exceptions it finds to exception tables, to await further analysis

## Yet to implement

- business rules step, between integration and load_to_target
- rollback
- Functional testing, which will be run in situ within a Sirius environment, utiliising establishes Sirius test behaviours


## DB connections for clients eg PyCharm and DataGrip:
```
db:   casrecmigration
host: localhost
port: 6666
user: casrec
pass: casrec
schema: etl1

db:   sirius
host: localhost
port: 5555
user: api
pass: api
schema: etl2

db:   sirius project postgres
host: localhost
port: 5432
user: api
pass: api
schema: public
```

If you don't see the tables in datagrip/pycharm db client, go across to 'schemas' and check that you have all necessary schemas checked (in this case `etl1`)

## Reset DB fixtures on sirius manually
```
wget https://github.com/ministryofjustice/opg-ecs-helper/releases/download/v0.2.0/opg-ecs-helper_Darwin_x86_64.tar.gz -O $HOME/opg-ecs-helper.tar.gz
sudo tar -xvf $HOME/opg-ecs-helper.tar.gz -C /usr/local/bin
sudo chmod +x /usr/local/bin/ecs-runner
cd terraform
export TF_WORKSPACE=development
terraform apply -target=local_file.output
# Open the file and change the user to a role you can assume
ecs-runner -task reset-api -timeout 600
ecs-runner -task migrate-api -timeout 600
ecs-runner -task import-fixtures-api -timeout 600
```

