import json
from pathlib import Path

# Ensure query JSON builders return valid JSON
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from queries import (
    build_tasks_query,
    build_stories_query,
    build_align_tasks_query,
)

def test_queries_are_valid_json():
    json.loads(build_tasks_query())
    json.loads(build_stories_query())
    json.loads(build_align_tasks_query())
