import types
from fibery_api import command_result, unwrap_entities

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


def test_command_result_with_error():
    resp = DummyResp({"success": False, "result": {"error": "bad"}})
    assert command_result(resp) is None


def test_unwrap_entities_with_wrapper():
    assert unwrap_entities({"data": [1, 2], "meta": {}}) == [1, 2]


def test_unwrap_entities_without_wrapper():
    assert unwrap_entities([3]) == [3]
