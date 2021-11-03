git remote add merging_repo https://github.com/ministryofjustice/opg-data-casrec-migration-mappings.git
git fetch merging_repo --tags
git merge --allow-unrelated-histories merging_repo/main
