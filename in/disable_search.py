import requests
import json
import csv

headers = {'Authorization':'Token -------','Content-Type': 'application/json', 'User-Agent': 'darafei@kontur.io search disabler script'}

def disable_search_in(schema):
    chunk = [{"command":"fibery.schema/batch", "args":{"commands":[{"command":"schema.type/set-meta", "args":{"name":schema, "key":"search/disabled", "value":True}}]}}]
    print(chunk)
    r = requests.post("https://kontur.fibery.io/api/commands", data=json.dumps(chunk), headers=headers)
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



print(requests.get("https://kontur.fibery.io/api/search/reindex", headers=headers))
