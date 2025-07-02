"""Helper functions for Fibery API interactions."""

from typing import Any
import structlog


def command_result(response: Any) -> Any:
    """Return the ``result`` section from a Fibery command response.

    If the response does not contain a ``result`` key, log the entire body and
    return ``None``.
    """
    log = structlog.get_logger(__name__)
    data = response.json()
    if isinstance(data, list):
        data = data[0]
    if "result" not in data:
        log.error("Malformed Fibery response", body=data)
        return None
    return data.get("result")
