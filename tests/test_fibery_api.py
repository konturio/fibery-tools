import types
from fibery_api import command_result

class DummyResp:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

def test_command_result_with_list():
    resp = DummyResp([{"result": 123}])
    assert command_result(resp) == 123

def test_command_result_with_dict():
    resp = DummyResp({"result": "ok"})
    assert command_result(resp) == "ok"
