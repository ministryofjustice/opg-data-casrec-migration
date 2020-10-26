#!/bin/bash

echo '-- Running FIXTURES --'
python3 fixtures.py
echo '-- Running LOAD --'
python3 load.py
