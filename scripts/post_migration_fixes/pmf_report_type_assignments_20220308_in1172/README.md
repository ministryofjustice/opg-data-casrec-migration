Run in the numbered order shown.

The first migration removes ALL annual_report_type_assignments records created by the migration.

The second adds annual_report_type_assignments records for each latest PENDING report.

If they are run in the incorrect order, the delete script will remove everything added by the insert script.