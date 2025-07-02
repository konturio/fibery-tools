"""Disable search for selected Fibery types."""

import requests
import json
from config_loader import import_config
from log import get_logger

TOKEN, FIBERY_BASE_URL = import_config("TOKEN", "FIBERY_BASE_URL")
log = get_logger(__name__)

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "search disabler script",
}

def disable_search_in(schema: str) -> None:
    """Disable search indexing for schema type ``schema``."""
    chunk = [
        {
            "command": "fibery.schema/batch",
            "args": {
                "commands": [
                    {
                        "command": "schema.type/set-meta",
                        "args": {"name": schema, "key": "search/disabled", "value": True},
                    }
                ]
            },
        }
    ]
    log.info(chunk)
    r = requests.post(
        f"{FIBERY_BASE_URL}/api/commands", data=json.dumps(chunk), headers=headers
    )
    log.info(r.text)
    
def main() -> None:
    """Disable search for predefined schemas."""
    schemas = [
        "KPI/Personal KPI",
        "KPI/Teams KPI",
        "KPI/Sprint commitments",
        "Candidate salary expectations/Salary expectation",
        "Finance/Salary change",
        "GitHub/Pull Request",
        "GitHub/Branch",
        "GitHub/Member",
        "Platform GitLab/Merge Request",
        "Platform GitLab/Branch",
        "vacations/dayon",
        "vacations/vacation",
        "vacations/sick",
        "KPI/Time Utilization",
    ]
    for schema in schemas:
        disable_search_in(schema)

    log.info(requests.get(f"{FIBERY_BASE_URL}/api/search/reindex", headers=headers))


if __name__ == "__main__":
    main()
