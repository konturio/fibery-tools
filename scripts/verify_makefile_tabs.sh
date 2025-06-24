#!/bin/sh
set -e
if [ -f Makefile ]; then
    if grep -n '^[ ]\+' Makefile >/dev/null; then
        echo "Makefile uses spaces instead of tabs" >&2
        exit 1
    fi
fi
