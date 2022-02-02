#!/bin/bash
echo "Running tranform unit tests - "
python3 -m pytest migration_steps/transform_casrec/transform/transform_tests --cov-fail-under=85
echo "Running shared unit tests - "
python3 -m pytest migration_steps/shared/shared_tests