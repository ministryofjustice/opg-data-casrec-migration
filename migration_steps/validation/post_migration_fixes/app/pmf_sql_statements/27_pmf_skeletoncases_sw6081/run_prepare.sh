#!/bin/bash
set -e

export RUNLIMIT=5000

# Part 1 - do cases without documens ~49,120
export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=0
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=5000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=10000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=15000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=20000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=25000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=30000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=35000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=40000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_nodocuments.sql -v runId=$RUN_ID -v notePrefix='SW6081 part 1: clients without documents' -v runLimit=$RUNLIMIT -v runOffset=45000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

# Part 2 - now do cases with documens ~68,951
export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=0
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=5000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=10000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=15000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=20000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=25000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=30000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=35000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=40000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=45000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=50000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=55000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=60000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

export RUN_ID=`psql -qtAXc "SELECT nextval('deleted_cases_sw6081.deleterun_id_seq')"`
psql -f ./sw6081/select_cases_with_docs.sql -v runId=$RUN_ID -v notePrefix='SW6081: clients with documents' -v runLimit=$RUNLIMIT -v runOffset=65000
psql -f ./sw6081/calc_last_activity.sql -v runId=$RUN_ID
psql -f ./sw6081/save_audit_data.sql -v runId=$RUN_ID

psql -c 'SELECT * FROM deleted_cases_sw6081.results ORDER BY delete_table ASC;'