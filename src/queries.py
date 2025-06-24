"""Helper functions to build Fibery query JSON."""

from __future__ import annotations

import json
from typing import Dict, Any


_ASSIGNMENTS_SELECT: Dict[str, Any] = {
    "q/from": ["assignments/assignees"],
    "q/select": {
        "fibery/id": ["fibery/id"],
        "fibery/public-id": ["fibery/public-id"],
        "user/name": ["user/name"],
        "fibery/rank": ["fibery/rank"],
        "user/email": ["user/email"],
        "avatar/avatars": {
            "q/from": ["avatar/avatars"],
            "q/limit": "q/no-limit",
            "q/select": {
                "fibery/id": ["fibery/id"],
                "fibery/name": ["fibery/name"],
                "fibery/content-type": ["fibery/content-type"],
                "fibery/secret": ["fibery/secret"],
            },
        },
    },
    "q/order-by": [[["user/name"], "q/asc"]],
    "q/limit": "q/no-limit",
}

_USER_TASKS_SELECT: Dict[str, Any] = {
    "q/from": ["user/Tasks"],
    "q/select": {
        "fibery/id": ["fibery/id"],
        "fibery/public-id": ["fibery/public-id"],
        "Tasks/name": ["Tasks/name"],
        "user/project": {
            "fibery/id": ["user/project", "fibery/id"],
            "fibery/rank": ["user/project", "fibery/rank"],
            "fibery/public-id": ["user/project", "fibery/public-id"],
            "Tasks/name": ["user/project", "Tasks/name"],
            "workflow/state": {
                "enum/name": ["user/project", "workflow/state", "enum/name"],
            },
        },
        "workflow/state": {
            "fibery/id": ["workflow/state", "fibery/id"],
            "fibery/public-id": ["workflow/state", "fibery/public-id"],
            "enum/name": ["workflow/state", "enum/name"],
        },
        "fibery/rank": ["fibery/rank"],
    },
    "q/order-by": [[["fibery/rank"], "q/asc"]],
    "q/limit": "q/no-limit",
}

_CONTRACT_SELECT: Dict[str, Any] = {
    "fibery/id": ["user/Contract", "fibery/id"],
    "fibery/public-id": ["user/Contract", "fibery/public-id"],
    "Tasks/name": ["user/Contract", "Tasks/name"],
    "Tasks/Deadline": ["user/Contract", "Tasks/Deadline"],
    "workflow/state": {
        "enum/name": ["user/Contract", "workflow/state", "enum/name"],
    },
}

_PROJECT_SELECT: Dict[str, Any] = {
    "fibery/id": ["user/project", "fibery/id"],
    "fibery/rank": ["user/project", "fibery/rank"],
    "fibery/public-id": ["user/project", "fibery/public-id"],
    "Tasks/name": ["user/project", "Tasks/name"],
    "workflow/state": {
        "enum/name": ["user/project", "workflow/state", "enum/name"],
    },
}

_SPRINT_SELECT: Dict[str, Any] = {
    "Tasks/When": ["user/Sprint", "Tasks/When"],
    "Tasks/name": ["user/Sprint", "Tasks/name"],
}


def _base_select() -> Dict[str, Any]:
    """Return fields common for task and user story queries."""
    return {
        "Tasks/name": ["Tasks/name"],
        "__status": ["workflow/state", "enum/name"],
        "ICE": ["Tasks/ICE Score"],
        "Priority": ["Tasks/Priority Int"],
        "assignments/assignees": _ASSIGNMENTS_SELECT,
        "fibery/creation-date": ["fibery/creation-date"],
        "fibery/id": ["fibery/id"],
        "fibery/modification-date": ["fibery/modification-date"],
        "fibery/public-id": ["fibery/public-id"],
        "user/Tasks": _USER_TASKS_SELECT,
        "user/Sprint": _SPRINT_SELECT,
    }


def build_tasks_query() -> str:
    """Return JSON query for ``Tasks/Task`` entities."""

    select = _base_select()
    select.update(
        {
            "Tasks/Actual~Finish": ["Tasks/Actual~Finish"],
            "Tasks/Actual~start": ["Tasks/Actual~start"],
            "Tasks/Deadline": ["Tasks/Deadline"],
            "Tasks/Verified by QA": ["Tasks/Verified by QA"],
            "Tasks/Story Point float": ["Tasks/Story Point float"],
            "Tasks/Skip QA": ["Tasks/Skip QA"],
            "user/Contract": _CONTRACT_SELECT,
            "user/project": _PROJECT_SELECT,
        }
    )

    query = {
        "command": "fibery.entity/query",
        "args": {
            "query": {
                "q/from": "Tasks/Task",
                "q/select": select,
                "q/offset": 0,
                "q/limit": "q/no-limit",
            },
            "params": {},
        },
    }
    return json.dumps(query)


def build_stories_query() -> str:
    """Return JSON query for ``Tasks/User Story`` entities."""

    query = {
        "command": "fibery.entity/query",
        "args": {
            "query": {
                "q/from": "Tasks/User Story",
                "q/select": _base_select(),
                "q/offset": 0,
                "q/limit": "q/no-limit",
            },
            "params": {},
        },
    }
    return json.dumps(query)


def build_align_tasks_query() -> str:
    """Return JSON query used by ``align`` script."""

    fields = [
        "fibery/id",
        "fibery/public-id",
        "Tasks/name",
        "Tasks/Branch Name",
        "fibery/creation-date",
        "fibery/modification-date",
        "Tasks/Actual~Finish",
        "Tasks/Actual~start",
        "Tasks/Actual Test Start",
        "Tasks/Verified by QA",
        "Tasks/Skip QA",
    ]
    select = {f: [f] for f in fields}
    select["__status"] = ["workflow/state", "enum/name"]

    query = [
        {
            "command": "fibery.entity/query",
            "args": {
                "query": {
                    "q/from": "Tasks/Task",
                    "q/select": select,
                    "q/offset": 0,
                    "q/limit": "q/no-limit",
                },
                "params": {},
            },
        }
    ]
    return json.dumps(query)

