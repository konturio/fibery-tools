import requests
import json

try:
    from config import TOKEN, FIBERY_BASE_URL
except ImportError as exc:  # pragma: no cover - configuration must be supplied
    raise SystemExit(
        "Missing config.py. Copy config.py.example and provide real values."
    ) from exc

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "search disabler script",
}

def disable_search_in(schema):
    chunk = [{"command":"fibery.schema/batch", "args":{"commands":[{"command":"schema.type/set-meta", "args":{"name":schema, "key":"search/disabled", "value":True}}]}}]
    print(chunk)
    r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=json.dumps(chunk), headers=headers)
    print(r.text)
    
disable_search_in("KPI/Personal KPI")
disable_search_in("KPI/Teams KPI")
disable_search_in("KPI/Sprint commitments")
disable_search_in("Candidate salary expectations/Salary expectation")
disable_search_in("Finance/Salary change")
disable_search_in("GitHub/Pull Request")
disable_search_in("GitHub/Branch")
disable_search_in("GitHub/Member")
disable_search_in("Platform GitLab/Merge Request")
disable_search_in("Platform GitLab/Branch")
disable_search_in("vacations/dayon")
disable_search_in("vacations/vacation")
disable_search_in("vacations/sick")
disable_search_in("KPI/Time Utilization")



print(requests.get(f"{FIBERY_BASE_URL}/api/search/reindex", headers=headers))
