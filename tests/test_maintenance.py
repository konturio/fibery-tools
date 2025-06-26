import json
import sys
import types

# Provide a stub requests module before importing align
sys.modules['requests'] = types.ModuleType('requests')
sys.modules['requests'].post = lambda *args, **kwargs: None

from align import reset_formula_fields, requests

class DummyResponse:
    def __init__(self):
        self.text = ""

def test_reset_formula_fields_sends_request(monkeypatch):
    calls = {}

    def fake_post(url, data=None, headers=None):
        calls["url"] = url
        calls["data"] = data
        calls["headers"] = headers
        return DummyResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    reset_formula_fields([("T", "F")])

    payload = json.loads(calls["data"])
    assert payload[0]["command"] == "fibery.schema/batch"
    assert calls["url"].endswith("/api/commands")

