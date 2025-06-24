import requests
import json
import re

headers = {'Authorization':'Token ---getyourown-------------','Content-Type': 'application/json', 'User-Agent': 'task branch name and actual start time fixer script'}

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
    r = requests.post("https://kontur.fibery.io/api/commands", data=json.dumps(update_tasks_command), headers=headers)
    print(r.text)

json.loads(get_tasks_command)
r = requests.post("https://kontur.fibery.io/api/commands", data=get_tasks_command, headers=headers)
tasks = r.json()[0]['result']

def removeSequenceOf(symbol, string):
  filtered = filter(lambda s: s != '', string.split(symbol))
  return symbol.join(filtered)
def branch_name(task):
  cleanedName = ''
  if task.get("Tasks/name",''):
    cleanedName = re.sub(r'[^(\w|\d|\-)]|[()\[\]\{\}]', '-', task.get("Tasks/name",'').strip().lower())
  withoutRepeated = removeSequenceOf('-', cleanedName)
  return task["fibery/public-id"] + '-' + withoutRepeated

#   return task["fibery/public-id"]+'_'+ task["Tasks/name"].lower().replace('"',"").replace("'","").replace("#","").replace(' ','_').replace('[','').replace(']','').replace('(','').replace(')','').replace(':',"").replace('@','_at_').replace('__',"_")
#    cleanedName = re.sub(r'[^(\w|\d|\s)]', '', task["Tasks/name"].strip().lower());
#    result = filter(lambda s: s != '', cleanedName.split(' '));
#    return task["fibery/public-id"] + '_' + '_'.join(result);

for task in tasks:
    #print(task)
    changed = False
    if (task['__status'] == 'In Progress' or task['__status'] == 'Review' or task['__status'] == 'In Testing' or task['__status'] == 'To Test') and task['Tasks/Actual~start'] is None:
        task['Tasks/Actual~start'] = task['fibery/modification-date']
        changed = True
    if task['__status'] == 'Done' and task['Tasks/Actual~Finish'] is None:
        task['Tasks/Actual~Finish'] = task['fibery/modification-date']
        changed = True
    if task['__status'] == 'Closed' and task['Tasks/Actual~Finish'] is None:
        task['Tasks/Actual~Finish'] = task['fibery/modification-date']
        changed = True
    if task['__status'] == 'In Testing' and task['Tasks/Actual Test Start'] is None:
        task['Tasks/Actual Test Start'] = task['fibery/modification-date']
        changed = True
    if task['__status'] == 'Verified by QA' and not task['Tasks/Verified by QA']:
        task['Tasks/Verified by QA'] = True
        changed = True
    if task['__status'] == 'Open' and task['Tasks/Verified by QA']:
        task['Tasks/Verified by QA'] = False
        changed = True
    if task['__status'] == 'Closed' and not task['Tasks/Skip QA']:
        task['Tasks/Skip QA'] = True
        changed = True
    if task['Tasks/Actual~Finish'] is not None and task['Tasks/Actual~start'] is None:
        task['Tasks/Actual~start'] = task['fibery/creation-date']
        changed = True
    if task['Tasks/Branch Name'] != branch_name(task):
        task['Tasks/Branch Name'] = branch_name(task)
        changed = True

    if changed:
        print(task)
        update_task(task)

        
    ##update_task({'fibery/id': 'b37845c0-4c96-11e9-8199-61f8d753595e', 'Tasks/name': 'Super name_updated'})
