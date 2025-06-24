# Fibery tools

Each file has a key in start, fill it in to use.

fibery_align.py - runs in endless loop and updates fields that don't make sense

fibery_workflow.py - generates graphviz dependencies for all the tasks, 
and a people_working_on.json with current tasks of everyone
```
python3 fibery_workflow.py | dot -v -Tsvg > tasks.svg
```

slack_standup.py - sends slack notification based on people_working_on.json
