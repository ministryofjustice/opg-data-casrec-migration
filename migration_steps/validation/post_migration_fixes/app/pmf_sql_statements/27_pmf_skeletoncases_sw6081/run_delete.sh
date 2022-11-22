#!/bin/bash

CONFIRM="n"

export RUN_MIN_ID=`psql -qtAXc "SELECT MIN(id) FROM deleted_cases_sw6081.run"`
export RUN_MAX_ID=`psql -qtAXc "SELECT MAX(id) FROM deleted_cases_sw6081.run"`

read -rp "Run ID? ($RUN_MIN_ID-$RUN_MAX_ID): " RUN_ID
echo $RUN_ID

if ! [[ "$RUN_ID" =~ ([0-9]+) ]];
then
    echo "Not a number... exiting"; exit 1
fi

export RUN_EXISTS=`psql -qtAXc "SELECT COUNT(1) FROM deleted_cases_sw6081.run WHERE id = $RUN_ID"`

if [ $RUN_EXISTS != 1 ]
then
    echo "No run by that ID... exiting"
    exit 1
fi

clear

echo -e "Delete run $RUN_ID will delete the following data:\n\nnote: rows from the documents table are not deleted at this stage\n"

psql -tc "
SELECT
    CASE WHEN delete_table = 'persons_clients_audit'
        THEN 'persons (CLIENTS)'
        ELSE delete_table
    END,
    run_$RUN_ID
FROM deleted_cases_sw6081.results
WHERE delete_table != 'documents'
AND run_$RUN_ID > 0
ORDER BY delete_table ASC"

read -rp "ARE YOU SURE? (y/n) [n]: " CONFIRM
if [ "$CONFIRM" == "y" ]
then
    echo $CONFIRM
    echo "Running delete script for delete run $RUN_ID"
    psql -f ./sw6081/delete.sql -v runId=$RUN_ID
    psql -c "UPDATE deleted_cases_sw6081.run SET deleted_at = CURRENT_TIMESTAMP(0) WHERE id = $RUN_ID"
else
    echo $CONFIRM
    echo "exiting"
fi

