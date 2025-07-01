try:
    import requests
except ImportError:  # pragma: no cover - requests may be absent during tests
    class requests:
        pass
import json
import re
from config_loader import import_config

FIBERY_BASE_URL, TOKEN = import_config("FIBERY_BASE_URL", "TOKEN")


headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "task branch name and actual start time fixer script",
}

get_tasks_command = """[
 {
 "command": "fibery.entity/query",
 "args": {
 "query": {
 "q/from": "Tasks/Task",
 "q/select": {
 "fibery/id": ["fibery/id"],
 "fibery/public-id": ["fibery/public-id"],
 "Tasks/name": ["Tasks/name"],
 "Tasks/Branch Name": ["Tasks/Branch Name"],
 "fibery/creation-date": ["fibery/creation-date"],
 "fibery/modification-date": ["fibery/modification-date"],
 "Tasks/Actual~Finish": ["Tasks/Actual~Finish"],
 "Tasks/Actual~start": ["Tasks/Actual~start"],
 "Tasks/Actual Test Start": ["Tasks/Actual Test Start"],
 "Tasks/Verified by QA": ["Tasks/Verified by QA"],
 "Tasks/Skip QA": ["Tasks/Skip QA"],
 "__status":["workflow/state","enum/name"] 
 },
 "q/offset": 0,
 "q/limit": "q/no-limit"
 },
 "params": {}
 }
 }
]"""


def reset_formula_fields(fields):
    """Remove disabled marks from formula fields."""
    for holder_type, field_name in fields:
        payload = [
            {
                "command": "fibery.schema/batch",
                "args": {
                    "commands": [
                        {
                            "command": "schema.field/delete-meta",
                            "args": {
                                "holder-type": holder_type,
                                "name": field_name,
                                "key": "formula/disabled?",
                            },
                        },
                        {
                            "command": "schema.field/delete-meta",
                            "args": {
                                "holder-type": holder_type,
                                "name": field_name,
                                "key": "formula/disable-reason",
                            },
                        },
                    ]
                },
            }
        ]
        requests.post(
            f"{FIBERY_BASE_URL}/api/commands",
            data=json.dumps(payload),
            headers=headers,
        )

def update_task(task):
    if "__status" in task:
        del task["__status"]
    if "fibery/modification-date" in task:
        del task["fibery/modification-date"]
    if "fibery/creation-date" in task:
        del task["fibery/creation-date"]
    if "fibery/public-id" in task:
        del task["fibery/public-id"]
    update_tasks_command = [
        {
            "command": "fibery.entity/update",
            "args": {
                "type": "Tasks/Task",
                "entity": task
            }
        }
    ]
#    print(update_tasks_command)
    r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=json.dumps(update_tasks_command), headers=headers)
    print(r.text)


def main():
    json.loads(get_tasks_command)
    r = requests.post(
        f"{FIBERY_BASE_URL}/api/commands",
        data=get_tasks_command,
        headers=headers,
    )
    try:
        tasks = r.json()[0]["result"]
    except Exception:
        sys.stderr.write(r.text)
        return

    # Reset formulas that may be disabled due to endless loop errors.
    reset_formula_fields([
        ("Tasks/User Story", "Tasks/ICE Score"),
        ("fibery/user", "user/Estimate scaling intercept"),
    ])

    for task in tasks:
        changed = False
        if (
            task["__status"] in ["In Progress", "Review", "In Testing", "To Test"]
            and task["Tasks/Actual~start"] is None
        ):
            task["Tasks/Actual~start"] = task["fibery/modification-date"]
            changed = True
        if task["__status"] == "Done" and task["Tasks/Actual~Finish"] is None:
            task["Tasks/Actual~Finish"] = task["fibery/modification-date"]
            changed = True
        if task["__status"] == "Closed" and task["Tasks/Actual~Finish"] is None:
            task["Tasks/Actual~Finish"] = task["fibery/modification-date"]
            changed = True
        if (
            task["__status"] == "In Testing"
            and task["Tasks/Actual Test Start"] is None
        ):
            task["Tasks/Actual Test Start"] = task["fibery/modification-date"]
            changed = True
        if task["__status"] == "Verified by QA" and not task["Tasks/Verified by QA"]:
            task["Tasks/Verified by QA"] = True
            changed = True
        if task["__status"] == "Open" and task["Tasks/Verified by QA"]:
            task["Tasks/Verified by QA"] = False
            changed = True
        if task["__status"] == "Closed" and not task["Tasks/Skip QA"]:
            task["Tasks/Skip QA"] = True
            changed = True
        if (
            task["Tasks/Actual~Finish"] is not None
            and task["Tasks/Actual~start"] is None
        ):
            task["Tasks/Actual~start"] = task["fibery/creation-date"]
            changed = True
        if task["Tasks/Branch Name"] != branch_name(task):
            task["Tasks/Branch Name"] = branch_name(task)
            changed = True

        if changed:
            print(task)
            update_task(task)

def removeSequenceOf(symbol, string):
    filtered = filter(lambda s: s != "", string.split(symbol))
    return symbol.join(filtered)


def branch_name(task):
    cleanedName = ""
    if task.get("Tasks/name", ""):
        cleanedName = re.sub(
            r"[^(\w|\d|\-)]|[()\[\]\{\}]",
            "-",
            task.get("Tasks/name", "").strip().lower(),
        )
    withoutRepeated = removeSequenceOf("-", cleanedName)
    return task["fibery/public-id"] + "-" + withoutRepeated

    # update_task({"fibery/id": "b37845c0-4c96-11e9-8199-61f8d753595e", "Tasks/name": "Super name_updated"})


if __name__ == "__main__":
    main()
