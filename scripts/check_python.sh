#!/bin/sh
set -e
files=$(find src -name '*.py')
python3 -m py_compile $files
