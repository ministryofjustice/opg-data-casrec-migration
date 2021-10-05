# opg-data-casrec-migration

## Purpose

The purpose of this repo is to house all the code that we will use to perform the casrec to sirius migration.
Having investigated AWS Glue & pyspark, we are using pandas dataframes to transform the data set into a form that can then be
ingested / inserted into Sirius platform.

We use AWS Localstack and postgres containers locally

## Setup from scratch


### Checkout

```bash
git clone git@github.com:ministryofjustice/opg-data-casrec-migration.git
```

All commands are from the root directory of `opg-data-casrec-migration` unless otherwise stated

### Install Python and dependencies

Download and install the latest version of Python (v3.9.6 at time of writing)

Install dependencies

```bash
pip install -r base_image/requirements.txt
```

### Grab Casrec dev data

For development we have a sample set of migration data in the same format as the files we will be receiving from Casrec (about 40 files). Sensitive data has been removed - hence we call this our 'anonymised csv data'.

You need to save these files to `data/anon_data/` on your development machine

```bash
mkdir -p data/anon_data

# copy .csv files within this dir (about 40 files)
```

The simplest way of doing this if you don't already have them, is to run the migrate.sh script as normal and choose 'yes' when asked
if you want to synchronise the data. This will clear out the folder and (make sure folder exists) and pull the files in from s3.

## Run a local migration

### Docker setup
```bash
# do a prune first if you reading this having had problems with migrate.sh
docker-compose down
docker system prune -a
```

### Running Migrate with migrate.sh (recommended)

```bash
./migrate.sh
```

#### Reloading source data (or skip)

You will be asked if you want to rebuild your local database from the source casrec csv files (building the schema which contains the data you're about to migrate). If you've made some changes and wish to restore, or if this is the first time you have run migrate.sh, click "y", otherwise there are Big time savings in selecying the default "n"

If you clicked "y" you'll now be asked if you want to syncronise the local data csv files from OPG Migrations dev on AWS S3. Again, if you have made changes to the local csv files, OR if this is a first run, click "y" otherwise there are big timesavings on "n"

If you do then you will need to enter your AWS Vault password and 2FA so you can connect to aws dev s3. If you don't have AWS Vault and 2FA set up, you'll need to grab someone in WebOps


Finally, you will be asked if you want to migrate all clients or just those managed by a certain Lay Team. You can leave this at default (all) unless you have a reason not to. See Filtering section below


#### No reload

You can also get the pipeline to run with no reload option.

- Add `~nr` somewhere in your commit message.

This is useful in a number of circumstances:
1) You have done a full run through and need to make a change to your PR
2) You want to avoid reload on preprod because it takes a very long time

You should not use this in pipeline if previous build didn't finish.


#### Filtering

By default, all lay clients will be migrated, but you can limit this to those of a certain Lay team in two ways:

In Env Vars (useful for pipeline/final production) - Specify a number 1-9 in `LAY_TEAM` in docker-compose or leave blank
At runtime (useful for dev) - you will be promped for a lay team when running `migrate.sh` enter 1-9 or hit return for default All. This will override the env var setting

## Install Sirius project (optional)

In order to see the results of a migration in the Sirius Front end you'll need the actual Sirius project:

Installing Sirius in a nutshell (refer to Sirius docs for more):

```
git clone git@github.com:ministryofjustice/opg-sirius.git
cd opg-sirius
```

#### Authenticate with AWS

To authenticate, first make sure you have a sirius dev profile with operator level access. This is used
to assume permissions in management to pull from management ECR (our repository for sirius images).

To check this, go into `~/.aws/config` and check if you have something that looks like
the following (with your name at the end):

```
[profile sirius-dev-operator]
region=eu-west-1
role_arn=arn:aws:iam::288342028542:role/operator
source_profile=identity
mfa_serial=arn:aws:iam::631181914621:mfa/firstname.lastname
```

```
aws-vault exec sirius-dev-operator -- make ecr_login
```

Setup sirius. *** Note *** Don't do the clean if you already have a recent setup or it will wipe it!!!

It is a surefire way to correct any drift in sirius though...

```
make clean && make dev-setup
```

You can re-run make dev-setup if it fails, without doing a make-clean

You should be able to view Sirius FE at http://localhost:8080
You should also be able to log in as case.manager@opgtest.com / Password1

If you can't log in, or if the site doesn't appear at all, but your containers seem to be up ok,
it sometimes helps to turn it off and on again:

```
make dev-stop
make dev-up
```

Then run this from the root of this repo and type "y" when asked if you want to migrate to `real local sirius`:

```
docker-compose down
./migrate.sh
```

The API tests will fail due to reindexing issues. This is expected. I can't currently think of a good way of calling
the reindex job from our job locally so just reindex as below (you will need this to perform searches anyway):

```
# (In Sirius local dev root)
docker-compose run --rm queue scripts/elasticsearch/setup.sh
```

Now you can run validation again and API tests will work:

```
docker-compose -f docker-compose.sirius.yml -f docker-compose.override.yml run --rm validation validation/validate.sh "$@"
```

To rerun again, you should reset the sirius databases. On the sirius side run the
following commands before rerunning your jobs:

```
make dev-up
```

This seems to restore from the last backup. If you have issues with this you may need to run these first:

```
make reset-databases
make ingest
```

### Troubleshooting

#### Local issues

- I am getting unexpected data based failures:
    - Try running the migrate script with resync.
    It is possible someone else has updated something that needs a different data set.

- I am getting weird docker issues:
    - Sometimes when switching between branches or when devs have modified paths to files then your existing
    images and containers will need refreshing as the code will be expecting one thing whilst the container
    volumes will have something else. If you can't immediately see the issue then it might be best to
    refresh everything. There's a helper script in root called `reset_local_env.sh` that you can run that will do
    a pretty hard cleanup for you without destroying other environments images (like sirius).

- I am still getting weird issues where it's saying files don't exist
    - Try and check the volume mounts are all correct in both the Dockerfiles (found in migration_steps folder) and
    in the dynamic volume entries in the `docker-compose.override.yml` file.

#### Pipeline based issues

- I am seeing issues with finding the task as part of the reset sirius job:
    - Check the time. If it's after 8pm then the env has been taken down.
    All sirius envs get taken down overnight to save money. If it's not then it is likely that the ECR
    images have been cleared up. We should be refreshing our sirius at least monthly.
    To do this:
        - Go to https://jenkins.opg.service.justice.gov.uk/job/Sirius/job/Create_Development_Environment/
        - Click on `build with parameters`
        - Enter `casmigrate` into the target_environment field
        - Pick 4 hours in drop down and leave other fields blank
        - Click build and wait for it to finish
        - Now in AWS sirius dev account, go to dynamo db and look for the WorkspaceCleanup table
        - Go to the items tab, find casmigrate and edit to epoch timestamp to be waaaaay in the future.
        This will stop it being deleted by cleanup jobs



## Testing your work

### Run the tests

```bash
# export test paths to PYTHONPATH with something like
export PYTHONPATH=[project root]/migration_steps/transform_casrec/transform/transform_tests:[project root]/migration_steps/transform_casrec/transform/app:[project root]/migration_steps/transform_casrec/transform

python3 -m pytest migration_steps/transform_casrec/transform/transform_tests
```

### Python linting - run precommit

Runs terraform_fmt, flake8, black etc

```bash
pre-commit run --all-files
```

## Other admin and utility scripts

### Importing latest spreadsheet and mapping definitions

Downloads the latest version of the file that is used to generate the mapping json docs.

You can sync as part of the normal migrate.sh job or alternatively, you can run the command below
(requires AWS Vault - if you don't have that, somebody in Ops should be able to help out).


```bash
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm sync_mapping_json python3 /scripts/sync_mapping_json/sync_mapping_json.py
```

There are two flags:

- `s3_source` is to decide whether to pull from staged or merged (defaults to merged).
- `version` is to decide whether to pull in specific version (defaults to latest)


## DB connections for clients eg PyCharm and DataGrip:
```
db:   casrecmigration
host: localhost
port: 6666
user: casrec
pass: casrec
schema: casrec_csv

db:   sirius
host: localhost
port: 5555
user: api
pass: api
schema: transform

db:   sirius project postgres
host: localhost
port: 5432
user: api
pass: api
schema: public
```

If you don't see the tables in datagrip/pycharm db client, go across to 'schemas' and check that you have all necessary schemas checked (in this case `casrec_csv`)

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

## Pull and anonymise a case from preprod

When we encounter issues in our data we want to be able to recreate them in our dev data so that we can debug locally.
We have an automated system to do this. It is a work in progress as the method to actually achieve
this is surprisingly complicated.

#### How to run it

From root directory, find the relevant caseref that you want to pull in and run:

```
./pull_and_anonymise_case.sh -c <caserefnnumber>
```

Some caveats to bear in mind before running this!

1) If anything doesn't work for any reason you need to reset your `/data/anon_data` by running migrate.sh
and selecting 'y' for both rebuild and sync of local data questions.
2) Don't rerun this script without resetting your anon_data folder first as above. It's not clever enough to not merge twice!
3) Always, always run a local `migrate.sh` first to check that the new data either loads correctly or
fails in the way your were expecting (if testing a failure from preprod).

#### How it works

- Initialises terraform and runs a job that populates a template. This stops us needing to hard code the subnet values etc.
- Kicks off a container that runs an ECS task. We have added the script to do the anonymising and moving of date to s3
to the etl0 (prepare job) and this gets called with an override.
- ECS task pulls the relevant data, anonymises it, formats it and puts it in a folder in s3 ready for download.
- We then kick off the synchronise script using preproduction as the environment parameter. This downloads the data locally,
formats it and merges it with our existing local data.

If you are happy with the data then you can manually add the files to the dev s3 bucket. We may automate this bit but for now I'd rather
we didn't accidentally overwrite the s3 bucket data.

This process is split across 3 python tasks and a terraform task. We have had to split it this way as we are not able to access DB
directly so have to access it through a separate ECS task.
Everything is controlled from the `pull_and_anonymise_case.sh` shell script.

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

#### load_s3

- Runs in local dev only. Takes the anonymised dev data and loads it into an S3 bucket on localdev, so that the next step will find the files in S3 as it does in AWS proper

#### prepare

- Runs some modifications on our local copy of sirius (dev only)
- Makes a copy of Sirius `api.public` schema called `pre_migration`. This will be used to hold our migration data before it is ready for loading, providing a final level of assurance that the data will 'fit' Sirius

#### load_casrec

- Reads the S3 files and saves them intact into a postgres database schema, one table per csv file
- Schema created: `casrecmigration.casrec_csv`

#### transform_casrec

- Reads data from the `casrec_csv` schema and performs a series of transformations on the columns
- Makes extensive use of pandas to perform the transformations
- Arrives at a schema more closely resembling the Sirius DB
- outputs schema `transform`

#### integration

- Copies `transform` to `integration`, which has added id columns to hold associated ids from Sirius
- Generates ID lookup tables from the Sirius DB
- Uses the lookup tables to transpose the corresponding Sirius ids into the integration schema

#### load_to_target

- takes the `pre_migrate` schema and performs a series of inserts where the data does not exist in Sirius, updates where it does.

#### validation

- Validates data at the DB layer, by comparing Sirius `api.public` with `pre_migrate`
- Returns a list of expected vs actual counts
- Saves any exceptions it finds to exception tables, to await further analysis

#### api tests
- Hits a selection of endpoints with a selection of data which we provide via csvs. We are testing per entity to make
sure that what we set out in the csvs matches the responses back from the APIs.

#### Yet to implement

- Business rules step, between integration and load_to_target
- Rollback

## Development environment

As of writing, we have a single development environment and do not do branch based builds. As such we need to fully reset
the environment between builds.

The development pipeline has the following features:

- Kicked off on raising a PR and subsequent pushes to an open PR (even in draft mode). As such only push to your PR
when you want it to build and be aware that this is blocking of other users!
- There is a cancel workflow job that intelligently cancels your own previous workflows that
aren't in the middle of terraform commands (and not other peoples).
- There is a waiter function that makes your job wait for another users job to finish so that we don't have two or
more builds running against the environment at the same time.
- We fully reset the envionment and restore the database as well as run in the fixtures and reset elasticache.
- We build new images, run local tests and do a full local run through with your commits code in and push them to ECR.
The reason for doing the full local run through is that it takes no extra time (we're waiting for sirius resets that are running in parallel) and
it can fail faster and not hold up the environment. It also avoids devs thinking it's an AWS environment issue when it isn't.
- We kick off a step function that sequences our steps and provides visual progress. Full list of steps can be found in the last section
- We notify the channel apon completion or failure of the workflow.
- Once workflow is completed, another dev can approve your PR and you can merge your code.
- No further job is run against Dev as the pipeline is single file and you are forced to rebase before merge so whatever
goes in is accurate representation of master.

#### Where to find everything...

Databases:

   - There are two databases we care about. One for the migration side and one for the sirius side. We have our own sirius environment.
    You can query them through a cloud9 instance. You can get the connection strings in cloud9 or by looking in RDS through the management console
    and the passwords are stored in secrets manager. The environments for dev are `casmigrate` (sirius)
    and `casrec-migration-development` (migration).

ECS:

   - The clusters that belong to us in this environment are `casmigrate` (sirius)
    and `casrec-migration-development` (migration). On migration side tasks get spun up by the step function so we
    should normally have 0 running.

Step function:

   - Search management console for step function and click on `casrec-mig-state-machine`.

Logs:

   - Find the logs under cloudwatch logs through management console. Our migration logs will
   be under `casrec-migration-development`

`
## Preproduction environment

We have two preproduction environments which are clones of each other. `casrecdmpp` and `casrecdmqa`.

`casrecdmpp` is our main preprod env and PRs should be run in as often as possible. `casrecdmqa` is a QA environment
that should only have builds that have passed in the other environment.

To do a full deploy to pre you should follow the following steps:

- Reset the sirius database. You can go to https://jenkins.opg.service.justice.gov.uk/job/Sirius/job/Deploy_to_CasRec_Data_Migration_Preproduction/
and click on `Build with Parameters` and pick `casrecdmpp` in the dropdown and and check the restore_database checkbox.
- Once complete you need to go to the most recent build through CirclCi and click the approval for kick off preprod.
- You can run it again by picking any previous preproduction workflow and restarting it from beginning. This works as it doesn't pull from build stage
but actually looks for the most recent image that has been pushed to ECR and tagged with master.

In all other respects the build is the same as in development. Same setup as above except that we use `casrecdmpp` as the sirius cluster
and `casrec-migration-preproduction` as the migration cluster.

#### Working with big data in preproduction

It can be frustrating debugging preprod because of the amount of data and how long everything takes. Here are some handy pointers:
- You can try using the `Pull and anonymise a case from preprod` steps as mentioned further up. Hopefully you can recreate the bug in local.
- You can run a cut down much much faster version of the pipeline that will use your local changes directly against pre
by building them and pushing to ECR. Simply rename `.circleci/config.yml` to `.circleci/config_orig.yml`
and then `.circleci/config_hack.yml` to `.circleci/config.yml`.

## QA environment

The QA environment works exactly the same as preproduction except it will only use code that has fully passed in preproduction.

- Kick it off by approving preproduction job or rerunning a QA job. It will pull the last image tagged with QA currently.
Images are tagged with QA on successful completion of preproduction run.

Circle doesn't have nice drop downs for selecting builds unfortunately so if we want selectable image builds then we will have to develop a
tiny script to kick off the job with a passed in param of the build number.

## Production environment

Production runs should not be kicked off automatically but we do want to make sure that the infra is deploying correctly
into prod before we try to run an actual migration there. As such, we have a Circle job that builds the infra in production albeit
with a cut down step function that only runs up until the transform stage.

There are some other 'safety features' that will need turning off when running the full real migration on prod:

- Switch out the short step function definition for the standard one.
- Turn on the SG rules for sirius DB and frontend by removing the `count` row on them which turns them off in production.
- Make sure the latest QA run has been tagged with `production` (this happens as final step of a successful QA run)
- Remove the `if` clauses in the `integration`, `sirius_load` and `validation` main shell scripts that prevent them from being run on production.
- Remove the check against `SIRIUS_DB_HOST` and `SIRIUS_FRONT_URL` that sets them to 'NOT_SET' in production
- In prepare step, take out the check against prod in the `prepare.sh` file

This is the full list of steps and these must be *CHECKED OFF* before running the real migration!!

The circle job to deploy will be kicked off from the command line to avoid people mis-clicking!

Adding the safe short step function to the prod pipeline will be done as a separate tiny ticket as
we want to check it all looks good before we run it. Once run, this bit of the README needs updating!

### Running Migration steps individually

Commands to run each step individually, still  via docker compose:

```bash
docker-compose run --rm load_s3 python3 load_s3_local.py
docker-compose run --rm prepare prepare/prepare.sh
docker-compose run --rm load_casrec python3 app.py
docker-compose run --rm transform_casrec python3 app.py --clear=True
docker-compose run --rm integration integration/integration.sh
docker-compose run --rm load_to_target python3 app.py
docker-compose run --rm validation validation/validate.sh
```

### Running the steps individually on AWS (ECS task runner)

We can kick off individual tasks if we so desire. This can be very useful for just running the API tests for example.

#### Example of running API tests against PreProduction

Initially we may want to trial data changes against PreProduction.

If you have modifications to scripts rather than just the data then you will have to push up the ECR image with your modifications to
ECR. To do this the simplest way is to do it yourself from the command line...

Login to ECR
```
aws-vault exec management -- aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 311462405659.dkr.ecr.eu-west-1.amazonaws.com
```

Set your version and aws registry

```
export AWS_REGISTRY=311462405659.dkr.ecr.eu-west-1.amazonaws.com
export VERSION=whatever-tag-you-want-to-create
```

Build the image locally and tag it (comment out extra images if you like):

```
docker-compose -f docker-compose.ci.yml build
```

Push the image to ECR:

```
docker-compose -f docker-compose.ci.yml push
```

We can now use the tagged image to run whatever we like from the command line. Remember that you only need to do this if changing the scripts.
If you're just adding some new data to Pre API tests that you want to check works then you can skip that entire first bit.

Get the tag of the ECR task you want to run. This is generally the commit tag. You can find this on last build to Preproduction in CircleCi.

```
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm task_runner ./run_ecs_task.sh \
-t ecr-tag-you-want-to-use \
-i validation \
-n etl5 \
-c "validation/api_tests.sh" \
-l casrec-migration-preproduction
```

Another example of running a task (this one loads casrec data on preprod):

```
aws-vault exec identity -- docker-compose -f docker-compose.commands.yml run --rm task_runner ./run_ecs_task.sh \
-t ecr-tag-you-want-to-use \
-i load-casrec \
-n etl1 \
-c python3,load_casrec/app/app.py \
-l casrec-migration-preproduction
```

#### Running the steps (Non-dockerised):

Note - the steps rely on data passed forward by the chain, so your safest bet is to run ./migrate  - but for debugging.

#### Install python requirements

```bash
pip3 install -r base_image/requirements.txt
pip install pre-commit
```

#### Set up python virtual environment

```bash
virtualenv venv
source venv/bin/activate

which python
> ...opg-data-casrec-migration/venv/bin/python
```

Several of the steps you can increase the log debugging level with -vv, -vvv etc

```bash
python3 migration_steps/load_s3_local.py
./migration_steps/prepare/prepare.sh -vv
python3 migration_steps/load_casrec/app/app.py
python3 migration_steps/transform_casrec/app/app.py -vv
./migration_steps/integration/integration.sh -vv
python3 migration_steps/load_to_target/app/app.py
./migration_steps/validation/validate.sh -vv
```

#### Deploying to an environment from a tagged image

From the root directory run the following:

`sh ./migrate_tagged_version.sh`

Follow the instructions carefully, being mindful to pick the relevant environment and tag.
You can then go and have a look at your job running in circle. During the get latest image stage,
it will actually override with the image you selected and you can check this in the 'show image' stage.
