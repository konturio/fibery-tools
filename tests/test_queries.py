import json
from pathlib import Path

# Ensure query JSON templates parse correctly
from queries import GET_TASKS_QUERY, GET_STORIES_QUERY

def test_queries_are_valid_json():
    json.loads(GET_TASKS_QUERY)
    json.loads(GET_STORIES_QUERY)
