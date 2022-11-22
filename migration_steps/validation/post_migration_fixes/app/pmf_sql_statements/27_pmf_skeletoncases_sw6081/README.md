-- ===================== PMF27 SW6081 =====================
-- Clean up of client data which OPG either should not have (was brought over with Livelink Migration)
-- ...or which violates data retention rules on ticket https://opgtransform.atlassian.net/browse/SW-6081

## A/C

### Original A/c on ticket sw6081
https://opgtransform.atlassian.net/browse/SW-6081
-- 1. Keep cases which now have an order attached. 
-- 2. Delete all cases without an order, which have no activity within the last 3 months
-- 3. Keep cases with activity within the past 3 months
-- 4. Keep the approx 380 cases within the spreadsheets attached to the above ticket
-- 5. Maintain a full copy of everything deleted in audit tables, ala other Migration Project 'PMF fixes'

### Update 14th Oct 2022
Delete clients without an order, irrespective of last activity "No order = delete"
https://docs.google.com/spreadsheets/d/1ISr32pT5Pl7Q-bRVwjwg2F92lbVgvQQL4gx82K584ek/edit#gid=1458605647

### Update 2
The 'exceptions' have now all been handled, therefore the 380 cases that were to be preserved can now also be deleted.

## Runbook

### Setup
CAUTION!!! RUN THIS ONLY ONCE, BEFORE FIRST RUN. IT WILL DELETE THE SCHEMA.

```bash
$ chmod 744 sw6081/*.sh
$ psql -f sw6081/setup_CAUTION_run_once.sql
```

### Run
```bash
# Create Run Data
$ ./sw6081/run_prepare.sh

# Delete (follow prompts)
$ ./sw6081/run_delete.sh
```

### Get results 
```bash
# print various delete runs
$ psql -c 'SELECT * FROM deleted_cases_sw6081.run'

# print deletion results
$ psql -c 'SELECT * FROM deleted_cases_sw6081.results'

# search for a client that was deleted
$ psql -c "SELECT * FROM deleted_cases_sw6081.run_clients WHERE caserecnumber = '1324903T'"
```