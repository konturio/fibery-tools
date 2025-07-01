import requests
import json
import csv

try:
    from config import TOKEN, FIBERY_BASE_URL
except ImportError as exc:  # pragma: no cover - configuration must be supplied
    raise SystemExit(
        "Missing config.py. Copy config.py.example and provide real values."
    ) from exc

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "rank patcher script",
}
def update_task(tasks):
    update_tasks_command = []
    for task in tasks:
        if "__status" in task:
            del task["__status"]
        if "fibery/modification-date" in task:
            del task["fibery/modification-date"]
        if "fibery/creation-date" in task:
            del task["fibery/creation-date"]
        if "fibery/public-id" in task:
            del task["fibery/public-id"]
        task_type = task["type"]
        del task["type"]
        
        update_tasks_command.append({
                "command": "fibery.entity/update",
                "args": {
                    "type": task_type,
                    "entity": task
                }
            })
        
    print(update_tasks_command)
    while update_tasks_command:
        chunk = update_tasks_command[:300]
        update_tasks_command = update_tasks_command[300:]
        r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=json.dumps(chunk), headers=headers)
        print(r.text)
    

min_rank  = -9000000000000000
max_rank  = -9999999999999999
max_new_rank = -99999999999999999
  

#﻿ домен значений для fibery/rank равен домену значений для js number
# Number.MAX_SAFE_INTEGER = (2^53 – 1) = 9007199254740991
# 9007199254740991 > 9008246374617369
 

task_by_id = {}

with open('tasknames.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['id', 'name', 'url', 'status', 'new_rank', 'orig_rank'])
    for task in reader:        
        new_rank = int(task['new_rank'])
        #if "User_" in task["url"]:
        #    continue
        #if new_rank > 0:
        real_id = task['id'].replace('-qa','')
        orig_rank = int(task["orig_rank"])       
        if orig_rank < min_rank:
            min_rank = orig_rank
        if orig_rank > max_rank:
            max_rank = orig_rank
        if new_rank > max_new_rank:
            max_new_rank = new_rank
        task = {
            "fibery/id": real_id,
            "new_rank": new_rank,
            "orig_rank": orig_rank,
            "type": "Tasks/User Story" if ("User_Story" in task["url"]) else "Tasks/Task"
        }
        
        if real_id in task_by_id:
            prev_rank = task_by_id[real_id]["new_rank"]            
            if prev_rank == 0:
                task["new_rank"] = new_rank
            elif new_rank == 0:
                task["new_rank"] = prev_rank
            else:
                task["new_rank"] = min(prev_rank, new_rank)
        task_by_id[real_id] = task
            
for task in task_by_id.values():
    if task["new_rank"] == 0:
        task["new_rank"] = task["orig_rank"] + max_new_rank - min_rank



#if max_rank > 0:
    #max_rank = -1

# split the date into correctly sorted runs
runs = [[]]
prev_rank = min_rank-1
for task_id, task in sorted(task_by_id.items(), key=lambda item: item[1]["orig_rank"]):
    if task["new_rank"] < prev_rank:
        runs.append([])        
    runs[-1].append(task)
    prev_rank = task["new_rank"]



sorted_result = []
prev_rank = min_rank
# merge the sorted runs and reassign the ranks
while runs:
    # pick smallest element from all runs' heads 
    runs = sorted(runs, key=lambda run: run[0]["new_rank"])
    task = runs[0].pop(0)
    if not runs[0]:
        runs.pop(0)
        
    if not sorted_result:
        task["fibery/rank"] = min_rank
        prev_rank = min_rank
        sorted_result.append(task)
        continue
       
    # pick rank between previous rank and next rank
    runs = sorted(runs, key=lambda run: run[0]["new_rank"])
    next_rank = max_rank
    if runs:        
        next_rank = runs[0][0]["orig_rank"]
    cur_rank = task["orig_rank"]
    
    if (cur_rank > next_rank or cur_rank < prev_rank) and next_rank > prev_rank:
        cur_rank = int(prev_rank + (next_rank-prev_rank)/10)
    #if cur_rank > prev_rank + 100000000000: # do not jump too high
    #    cur_rank = prev_rank + 100000000000
    if cur_rank <= prev_rank: # exit endless loop by enumerating naiively
        cur_rank = prev_rank + 10000
    
    # add to results
    task["fibery/rank"] = cur_rank
    sorted_result.append(task)
    prev_rank = cur_rank



print(sorted_result)
# flip it so top entries get changed first
sorted_result = sorted(sorted_result, key=lambda task: task["orig_rank"])
t = []
for i in sorted_result:
    if i["orig_rank"] != i["fibery/rank"]:        
        print(i)
        del i["orig_rank"]
        del i["new_rank"]
        t.append(i)
update_task(t)






#for run in runs:
#    print(run)



#for task_id, task in sorted(task_by_id.items(),key=lambda item: item[1]):
#    
#    update_task(task)
#    print(task_id, rank)

