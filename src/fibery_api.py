"""Helper functions for Fibery API interactions."""

from typing import Any


def command_result(response: Any) -> Any:
    """Return the ``result`` section from a Fibery command response."""
    data = response.json()
    if isinstance(data, list):
        data = data[0]
    return data.get("result")
