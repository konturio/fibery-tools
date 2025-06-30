#!/bin/sh
# Update Fibery tasks and render tasks.svg diagram.
set -e

python3 src/align.py | unflatten -l 2 -f -c 5 > tasks.dot
python3 src/patch_ranks.py &
(
    cp -f tasks.dot tasks_bck.dot
    cat tasks.dot | dot -Tsvg -v > tasks_new.svg
) &

sleep 10
wait
mv tasks_new.svg tasks.svg
