import json
from pathlib import Path

# Ensure query JSON templates parse correctly
from queries import GET_TASKS_QUERY, GET_STORIES_QUERY

def test_queries_are_valid_json():
    tasks = json.loads(GET_TASKS_QUERY)
    stories = json.loads(GET_STORIES_QUERY)
    assert isinstance(tasks, list) and tasks
    assert isinstance(stories, list) and stories
    assert tasks[0]["command"] == "fibery.entity/query"
    assert stories[0]["command"] == "fibery.entity/query"
