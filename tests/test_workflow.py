import contextlib
import io
import runpy
import sys
import types

# Create stub config module
sys.modules['config'] = types.ModuleType('config')
sys.modules['config'].FIBERY_BASE_URL = 'https://example.fibery.io'
sys.modules['config'].TOKEN = 'dummy'

# Prepare stub tasks
TASK = {
    "fibery/id": "t1",
    "fibery/public-id": "T1",
    "Tasks/name": "Test task",
    "Priority": 3,
    "ICE": 0,
    "__status": "Open",
    "Tasks/Story Point float": 1,
    "assignments/assignees": [{"fibery/id": "u1", "user/name": "User1"}],
    "user/Substories": [],
    "user/User Story": {},
    "user/Tasks": [],
    "Tasks/Deadline": None,
    "user/Contract": {},
    "Tasks/Verified by QA": False,
    "Tasks/Skip QA": False,
    "user/project": {},
    "Tasks/Actual~Finish": None,
    "user/Sprint": {"Tasks/name": "", "Tasks/When": None},
    "fibery/creation-date": "2023-01-01T00:00:00",
    "fibery/modification-date": "2023-01-02T00:00:00",
}

class DummyResponse:
    def __init__(self, data):
        self._data = data
        self.text = ""
    def json(self):
        return self._data

responses = [
    [{"success": True, "result": {"data": [TASK], "meta": {}}}],
    [{"success": True, "result": {"data": [], "meta": {}}}],
]

def fake_post(url, data=None, headers=None):
    return DummyResponse(responses.pop(0))

requests_mod = types.ModuleType('requests')
requests_mod.post = fake_post
sys.modules['requests'] = requests_mod

def test_workflow_does_not_create_qa_tasks(tmp_path, monkeypatch):
    sys.modules.pop('workflow', None)
    out = io.StringIO()
    monkeypatch.chdir(tmp_path)
    with contextlib.redirect_stdout(out):
        runpy.run_module('workflow', run_name='__main__')
    output = out.getvalue()
    assert '-qa' not in output
    assert 'Anastasiya' not in output
    assert 'Pavel' not in output
