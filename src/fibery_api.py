"""Helper functions for Fibery API interactions."""

from typing import Any
import structlog


def unwrap_entities(result: Any) -> list:
    """Return a list of entities from a Fibery command result.

    Newer versions of the Fibery API wrap returned entities in a
    ``{"data": [...], "meta": {...}}`` object.  Older versions returned a
    plain list.  This helper normalises both formats to a list so callers
    do not need to care which one they receive.
    """
    if isinstance(result, dict):
        if "data" in result:
            return result.get("data", [])
        return []
    return result


def command_result(response: Any) -> Any:
    """Return the ``result`` section from a Fibery command response.

    If the response does not contain a ``result`` key, log the entire body and
    return ``None``.
    """
    log = structlog.get_logger(__name__)
    data = response.json()
    if isinstance(data, list):
        data = data[0]

    if not data.get("success", True):
        log.error("Fibery command failed", body=data)
        return None

    if "result" not in data:
        log.error("Malformed Fibery response", body=data)
        return None

    return data.get("result")
