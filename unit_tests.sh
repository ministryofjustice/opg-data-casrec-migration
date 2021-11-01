#!/bin/bash
BASE_DIR=`dirname $0`

export PYTHONPATH=$BASE_DIR/migration_steps/transform_casrec/transform/transform_tests:$BASE_DIR/migration_steps/transform_casrec/transform/app:$BASE_DIR/migration_steps/transform_casrec/transform

# get last argument passed to script
file_or_directory=""
if [ $# -gt 0 ] ; then
    file_or_directory="${BASH_ARGV[0]}"
fi

# check whether it's a file or directory; if not, set a default
if [[ -z $file_or_directory && ! -f $file_or_directory && ! -d $file_or_directory ]] ; then
    # set default directory
    file_or_directory="./migration_steps/transform_casrec/transform/transform_tests/"
    args=$*
else
    # last arg is directory, store all args except that one
    args=${*%${!#}}
fi

echo "TEST FILES: "$file_or_directory

python3 -m pytest $args $file_or_directory
