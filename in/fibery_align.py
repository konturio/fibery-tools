import requests
import json
import dateutil.parser as dp
from graphviz import Digraph
from datetime import date
import datetime
import math
import sys
import csv

def aaa():
    now = datetime.datetime.now()

    headers = {'Authorization': 'Token ---------', 'Content-Type': 'application/json', 'User-Agent': 'darafei@kontur.io task charting reader'}

    get_tasks_command = """[
    {
        "command": "fibery.entity/query",
        "args": {
        "query": {
            "q/from": "Tasks/Task",
            "q/select": {
            "Tasks/Actual~Finish": [
                "Tasks/Actual~Finish"
            ],
            "Tasks/Actual~start": [
                "Tasks/Actual~start"
            ],
            "ICE": [
                "Tasks/ICE Score"
            ],
            "Priority": [
                "Tasks/Priority Int"
            ],
            "PERT95": [
                "Tasks/PERT 95% Confidence"
            ],
            "Tasks/Deadline": [
                "Tasks/Deadline"
            ],
            "Tasks/Verified by QA": [
                "Tasks/Verified by QA"
            ],
            "Tasks/Skip QA": [
                "Tasks/Skip QA"
            ],
            "Tasks/Commitment?": [
                "Tasks/Commitment?"
            ],
            "Tasks/Has active goals?": [
                "Tasks/Has active goals?"
            ],
            "Tasks/name": [
                "Tasks/name"
            ],
            "__status": [
                "workflow/state",
                "enum/name"
            ],
            "__task_type": [
                "Tasks/Task Type",
                "enum/name"
            ],
            "fibery/rank": [
                    "fibery/rank"
            ],
            "assignments/assignees": {
                "q/from": [
                "assignments/assignees"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "user/name": [
                    "user/name"
                ],
                "fibery/rank": [
                    "fibery/rank"
                ],
                "user/email": [
                    "user/email"
                ],
                "avatar/avatars": {
                    "q/from": [
                    "avatar/avatars"
                    ],
                    "q/limit": "q/no-limit",
                    "q/select": {
                    "fibery/id": [
                        "fibery/id"
                    ],
                    "fibery/name": [
                        "fibery/name"
                    ],
                    "fibery/content-type": [
                        "fibery/content-type"
                    ],
                    "fibery/secret": [
                        "fibery/secret"
                    ]
                    }
                }
                },
                "q/order-by": [
                [
                    [
                    "user/name"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            },
            "fibery/creation-date": [
                "fibery/creation-date"
            ],
            "fibery/id": [
                "fibery/id"
            ],
            "fibery/modification-date": [
                "fibery/modification-date"
            ],
            "fibery/public-id": [
                "fibery/public-id"
            ],
            "user/Contract": {
                "fibery/id": [
                "user/Contract",
                "fibery/id"
                ],
                "fibery/public-id": [
                "user/Contract",
                "fibery/public-id"
                ],
                "Tasks/Deadline": [
                "user/Contract",
                "Sales CRM/Deadline"
                ],
                "workflow/state": {
                "enum/name": [
                    "user/Contract",
                    "workflow/state",
                    "enum/name"
                ]
                }
            },
            "user/Tasks": {
                "q/from": [
                "user/Subtasks"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "Tasks/name": [
                    "Tasks/name"
                ],
                "user/project": {
                    "fibery/id": [
                    "user/project",
                    "fibery/id"
                    ],
                    "fibery/rank": [
                    "user/project",
                    "fibery/rank"
                    ],
                    "fibery/public-id": [
                    "user/project",
                    "fibery/public-id"
                    ],
                    "Tasks/name": [
                    "user/project",
                    "Tasks/name"
                    ],
                    "workflow/state": {
                    "enum/name": [
                        "user/project",
                        "workflow/state",
                        "enum/name"
                    ]
                    }
                },
                "workflow/state": {
                    "fibery/id": [
                    "workflow/state",
                    "fibery/id"
                    ],
                    "fibery/public-id": [
                    "workflow/state",
                    "fibery/public-id"
                    ],
                    "enum/name": [
                    "workflow/state",
                    "enum/name"
                    ]
                },
                "fibery/rank": [
                    "fibery/rank"
                ]
                },
                "q/order-by": [
                [
                    [
                    "fibery/rank"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            },
            "user/project": {
                "fibery/id": [
                "user/project",
                "fibery/id"
                ],
                "fibery/rank": [
                "user/project",
                "fibery/rank"
                ],
                "fibery/public-id": [
                "user/project",
                "fibery/public-id"
                ],
                "Tasks/name": [
                "user/project",
                "Tasks/name"
                ],
                "workflow/state": {
                "enum/name": [
                    "user/project",
                    "workflow/state",
                    "enum/name"
                ]
                }
            },
            "user/Sprint": {            
                "Tasks/When": [
                "user/Sprint",
                "Tasks/When"
                ],
                "Tasks/name": [
                "user/Sprint",
                "Tasks/name"
                ]
            },
            "user/User Story": {
                "assignments/assignees": {
                    "q/from": [
                    "user/User Story", "assignments/assignees"
                    ],
                    "q/select": {
                    "fibery/id": [
                        "fibery/id"
                    ],
                    "fibery/public-id": [
                        "fibery/public-id"
                    ],
                    "user/name": [
                        "user/name"
                    ],
                    "fibery/rank": [
                        "fibery/rank"
                    ],
                    "user/email": [
                        "user/email"
                    ]
                    },
                    "q/order-by": [
                    [
                        [
                        "user/name"
                        ],
                        "q/asc"
                    ]
                    ],
                    "q/limit": "q/no-limit"
                },
                "user/Substories": {
                "q/from": [
                "user/User Story",
                "user/Substories"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "Tasks/name": [
                    "Tasks/name"
                ],
                "workflow/state": {
                    "fibery/id": [
                    "workflow/state",
                    "fibery/id"
                    ],
                    "fibery/public-id": [
                    "workflow/state",
                    "fibery/public-id"
                    ],
                    "enum/name": [
                    "workflow/state",
                    "enum/name"
                    ]
                },
                "fibery/rank": [
                    "fibery/rank"
                ]
                },
                "q/order-by": [
                [
                    [
                    "fibery/rank"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            }
            }
            },
            "q/offset": 0,
            "q/limit": "q/no-limit"
        },
        "params": {}
        }
    }
    ]"""

    json.loads(get_tasks_command)
    r = requests.post("https://kontur.fibery.io/api/commands", data=get_tasks_command, headers=headers)
    try:
        tasks = r.json()[0]['result']
    except:
        sys.stderr.write(r.text)
        pass
    #sys.stderr.write(r.text)
    sys.stderr.write("Got tasks\n")
    sys.stderr.flush()

    get_stories_command = """[
    {
        "command": "fibery.entity/query",
        "args": {
        "query": {
            "q/from": "Tasks/User Story",
            "q/select": {
            "Tasks/name": [
                "Tasks/name"
            ],
            "__status": [
                "workflow/state",
                "enum/name"
            ],
            "ICE": [
                "Tasks/ICE Score"
            ], 
            "Priority": [
                "Tasks/Priority Int"
            ],
            "fibery/rank": [
                    "fibery/rank"
            ],            
            "Tasks/Commitment?": [
                "Tasks/Commitment?"
            ],
            "Tasks/Has active goals?": [
                "Tasks/Has active goals?"
            ],
            "assignments/assignees": {
                "q/from": [
                "assignments/assignees"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "user/name": [
                    "user/name"
                ],
                "fibery/rank": [
                    "fibery/rank"
                ],
                "user/email": [
                    "user/email"
                ]
                },
                "q/order-by": [
                [
                    [
                    "user/name"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            },
            "fibery/creation-date": [
                "fibery/creation-date"
            ],
            "fibery/id": [
                "fibery/id"
            ],
            "fibery/modification-date": [
                "fibery/modification-date"
            ],
            "fibery/public-id": [
                "fibery/public-id"
            ],
            "Tasks/Date Range": [
                "Tasks/Date Range"
            ],
            "user/Tasks": {
                "q/from": [
                "user/Tasks"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "Tasks/name": [
                    "Tasks/name"
                ],
                "user/project": {
                    "fibery/id": [
                    "user/project",
                    "fibery/id"
                    ],
                    "fibery/rank": [
                    "user/project",
                    "fibery/rank"
                    ],
                    "fibery/public-id": [
                    "user/project",
                    "fibery/public-id"
                    ],
                    "Tasks/name": [
                    "user/project",
                    "Tasks/name"
                    ],
                    "workflow/state": {
                    "enum/name": [
                        "user/project",
                        "workflow/state",
                        "enum/name"
                    ]
                    }
                },
                "workflow/state": {
                    "fibery/id": [
                    "workflow/state",
                    "fibery/id"
                    ],
                    "fibery/public-id": [
                    "workflow/state",
                    "fibery/public-id"
                    ],
                    "enum/name": [
                    "workflow/state",
                    "enum/name"
                    ]
                },
                "fibery/rank": [
                    "fibery/rank"
                ]
                },
                "q/order-by": [
                [
                    [
                    "fibery/rank"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            },
            
            "user/Substories": {
                "q/from": [
                "user/Substories"
                ],
                "q/select": {
                "fibery/id": [
                    "fibery/id"
                ],
                "fibery/public-id": [
                    "fibery/public-id"
                ],
                "Tasks/name": [
                    "Tasks/name"
                ],
                "workflow/state": {
                    "fibery/id": [
                    "workflow/state",
                    "fibery/id"
                    ],
                    "fibery/public-id": [
                    "workflow/state",
                    "fibery/public-id"
                    ],
                    "enum/name": [
                    "workflow/state",
                    "enum/name"
                    ]
                },
                "fibery/rank": [
                    "fibery/rank"
                ]
                },
                "q/order-by": [
                [
                    [
                    "fibery/rank"
                    ],
                    "q/asc"
                ]
                ],
                "q/limit": "q/no-limit"
            },
            "user/Sprint": {            
                "Tasks/When": [
                "user/Sprint",
                "Tasks/When"
                ],
                "Tasks/name": [
                "user/Sprint",
                "Tasks/name"
                ]
            }          
            },
            "q/offset": 0,
            "q/limit": "q/no-limit"
        },
        "params": {}
        }
    }
    ]"""

    json.loads(get_stories_command)
    r = requests.post("https://kontur.fibery.io/api/commands", data=get_stories_command, headers=headers)
    try:
        stories = r.json()[0]['result']
    except:
        sys.stderr.write(r.text)
        pass
    #sys.stderr.write(r.text)
    
    sys.stderr.write("Got user stories\n")
    sys.stderr.flush()

    tasks += stories

    dot = Digraph()
    dot.graph_attr["rankdir"] = "TB"
    #dot.graph_attr["rankdir"] = "LR"
    dot.graph_attr["newrank"] = "true"
    dot.graph_attr["nslimit"] = "10.0"
    #dot.graph_attr["nslimit1"] = "10.0"
    #dot.graph_attr["nodesep"] = "0.5"
    dot.graph_attr["nodesep"] = "1"

    # dot.graph_attr["nslimit"] = "50.0"
    #dot.graph_attr["concentrate"]="true"

    estimates = []

    dot.attr('node', shape='box')

    this_month = date.today().strftime("%Y-%m")
    today = date.today().strftime("%Y-%m-%d")


    def trim_date(d):
        a = d.split('T')[0]

        parsed_day = dp.parse(a)
        while parsed_day.isoweekday() > 5:
            parsed_day -= datetime.timedelta(days=1)
        a = parsed_day.strftime("%Y-%m-%d")
        if a < this_month:
            a = a[:7]
        return a


    def up_date(d):
        a = d.split('T')[0]
        parsed_day = dp.parse(a)
        while parsed_day.isoweekday() > 5:
            parsed_day += datetime.timedelta(days=1)
        a = parsed_day.strftime("%Y-%m-%d")
        return a


    def half_life(d):
        delta = (dp.parse(d) - now)
        if delta.total_seconds() > 0:
            return (now + delta / 2).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return d

    needed_blockers = set()
    deadlines = set()
    deadlines.add(this_month)

    hidden_tasks = set()
    tasks_by_id = {}
    to_test = set()
    deadline_half_lifes = {}


    def qa_id(i):
        return i + "-qa"


    qa_tasks = []

    users = set() 
    
    
    
    ephemeral_dependencies = set()
    
    for task in tasks:
        hl = "2999-12-30"
        skip_qa = task.get("Tasks/Skip QA", True)  # User stories don't have Skip QA
        task["__type"] = "Task"
        
        
        # substories block stories
        if "user/Substories" in task:
            task["user/Tasks"].extend(task["user/Substories"])
            
        # substories of the story block tasks of the story
        if "user/User Story" in task:
            # TODO: add these only if that does not create a cycle
            task["user/Tasks"].extend(task["user/User Story"]["user/Substories"])
            for story in task["user/User Story"]["user/Substories"]:
                ephemeral_dependencies.add((task["fibery/id"], story["fibery/id"]))
                
                
        # if there are self-dependencies for some reason, ignore them
        task["user/Tasks"] = [i for i in task["user/Tasks"] if i["fibery/id"] != task["fibery/id"]]
            
        
        if "__task_type" in task:
            if task["__task_type"] == "Production issue":
                task["Commitment?"] = True
            if task["__task_type"] == "Paperwork":
                task["Commitment?"] = True
                task["PERT95"] = 1
                skip_qa = True


        
        if "Tasks/Deadline" not in task:  # US have no deadline
            task["Tasks/Deadline"] = None
            task["__type"] = "User_Story"
        if "user/Contract" not in task:
            task["user/Contract"] = {"Tasks/Deadline": None}
        if "Tasks/Verified by QA" not in task:
            task["Tasks/Verified by QA"] = True
        if "user/project" not in task:
            task["user/project"] = {}
        if "Tasks/Actual~Finish" not in task:
            task["Tasks/Actual~Finish"] = None
        if "PERT95" not in task:
            task["PERT95"] = None
            
            
            
        if "user/User Story" not in task:
            task["user/User Story"] = task

        if not task["Priority"]:
            task["Priority"] = 5  # 5 is Normal priority

        task["__sprint_end"] = "9999-12-30"
        if task["__status"] == "Backlog":
            hl = "9999-12-30"


        if "Tasks/Date Range" in task:
            if task["Tasks/Date Range"] and not not task['Tasks/Deadline']:
                task['Tasks/Deadline'] = task["Tasks/Date Range"]["end"]
        if task["user/Sprint"]:
            if task["user/Sprint"]["Tasks/When"]:
                hl = task["user/Sprint"]["Tasks/When"]["end"]
                if not task['Tasks/Deadline']:
                    task['Tasks/Deadline'] = task["user/Sprint"]["Tasks/When"]["end"]
                elif task['Tasks/Deadline'] > task["user/Sprint"]["Tasks/When"]["end"]:
                    task['Tasks/Deadline'] = task["user/Sprint"]["Tasks/When"]["end"]
                task["__sprint_end"] = task["user/Sprint"]["Tasks/When"]["end"]
                deadlines.add(hl)            
            

        if task["user/Contract"]["Tasks/Deadline"]:
            hl = task["user/Contract"]["Tasks/Deadline"]
            if not task['Tasks/Deadline']:
                task['Tasks/Deadline'] = task["user/Contract"]["Tasks/Deadline"]
            elif task['Tasks/Deadline'] > task["user/Contract"]["Tasks/Deadline"]:
                task['Tasks/Deadline'] = task["user/Contract"]["Tasks/Deadline"]
            deadlines.add(hl)

        if task['Tasks/Deadline']:
            hl = min(hl, trim_date(task['Tasks/Deadline']))
            deadlines.add(hl)
        if task["__status"] == "Closed":
            hidden_tasks.add(task["fibery/id"])
            skip_qa = True
        if task["__status"] == "Canceled":
            hidden_tasks.add(task["fibery/id"])
            skip_qa = True
        if task["__status"] == "Done" and task["Tasks/Verified by QA"]:
            hidden_tasks.add(task["fibery/id"])
        if task["__status"] == "To Test":
            hidden_tasks.add(task["fibery/id"])
        if task["__status"] == "In Testing":
            hidden_tasks.add(task["fibery/id"])
        if task["__status"] == "To Deploy":
            hidden_tasks.add(task["fibery/id"])
        if task["__status"] == "Done":
            hidden_tasks.add(task["fibery/id"])
            skip_qa = True
        if task["__status"] == "Verified by QA":  # and task["Tasks/Verified by QA"]:
            hidden_tasks.add(task["fibery/id"])
        if not task["Tasks/name"]:
            task["Tasks/name"] = ""

        task['Tasks/Estimate'] = 8
        if task['PERT95']:
            pert = float(task['PERT95'])
            if pert < 1000000:
                task['Tasks/Estimate'] = pert

        task['Tasks/Estimate'] = float(task['Tasks/Estimate'])
        

#        if "workflow/state" in task["user/Contract"]:
#            if task["user/Contract"]["workflow/state"]["enum/name"] in ["Stopped", "Done"]:
#                hidden_tasks.add(task["fibery/id"])
#                skip_qa = True

#        if "workflow/state" in task["user/project"]:
#            if task["user/project"]["workflow/state"]["enum/name"] in ["Stopped", "Done"]:
#                hidden_tasks.add(task["fibery/id"])
#                skip_qa = True


        if not task["assignments/assignees"]:
            task["assignments/assignees"].append({'fibery/id': 'Unassigned', 'user/name': 'Unassigned'})

        deadline_half_lifes[task["fibery/id"]] = hl
        if task['Tasks/Actual~Finish']:
            deadlines.add(trim_date(task['Tasks/Actual~Finish']))

        deadlines.add(trim_date(task['fibery/creation-date']))
        for user in task["assignments/assignees"]:
            users.add(user['fibery/id'])

        if not skip_qa and not task["Tasks/Verified by QA"]:
            t = task.copy()
            t["fibery/id"] = qa_id(t["fibery/id"])
            t["Tasks/name"] += " - Verify"            
            t["__status"] = "Open"
            t["assignments/assignees"] = t["assignments/assignees"].copy()
            
            if task['__status'] in ('Backlog', 'Analysis', 'To Do', 'Blocked', 'In Progress', 'Review', 'Buffering'):
                t["__status"] = "Backlog"            

            # QAs from user story check things in it       

            qa = []
            qa_uuids = ('455f2f50-5627-11e9-bcdd-8aba22381101', 'b85ccda0-6373-11ea-8da1-c73fee560e63', '9eb77ce3-21a1-4fa3-a542-2720b99ee119', 'ce4b1672-ec57-4c65-9f03-306cc3f72103', '964aa50e-9d3f-4a5a-8d6a-fc669b4f675e','0f704204-0356-48f4-b00c-836a4b5fa053','dbe2bc80-cfea-11ed-9baf-8f3a93570365') # TODO: replace by checking "Quality assurance?" tag on user
            
            #if t['user/User Story']:
            for person in t["assignments/assignees"]:
                if person['fibery/id'] in qa_uuids:
                    qa.append(person)
                    task["assignments/assignees"].remove(person)
            if not qa:
                qa = [ # TODO: replace by checking "Quality assurance?" tag on user, unhardcode
                    {'fibery/id': '455f2f50-5627-11e9-bcdd-8aba22381101', 'user/name': 'Anastasia Artyukevich'},
                    {'fibery/id': 'b85ccda0-6373-11ea-8da1-c73fee560e63', 'user/name': 'Pavel Rytvinsky'}]
            # do not create the Verify task if all assignees are QAs, put them back
            if not task["assignments/assignees"]:
                task["assignments/assignees"] = qa
                continue
            t["assignments/assignees"] = qa            
            t['Tasks/Estimate'] = t['Tasks/Estimate'] / max(len(qa), 2)            
            t["user/Tasks"] = [{"fibery/id": task["fibery/id"]}]
            qa_tasks.append(t)
            deadline_half_lifes[t["fibery/id"]] = hl
  
    tasks += qa_tasks
    
    # all tasks have an assignee
    for task in tasks:
        if not task["assignments/assignees"]:
            task["assignments/assignees"].append({'fibery/id': 'Unassigned', 'user/name': 'Unassigned'})


    sys.stderr.write("Reformatted tasks\n")
    sys.stderr.flush()

    for task in tasks:
        tasks_by_id[task["fibery/id"]] = task

    for task in tasks:
        if "qa" not in task["fibery/id"]:
            for blocker in task["user/Tasks"]:
                if qa_id(blocker["fibery/id"]) in tasks_by_id:
                    blocker["fibery/id"] = qa_id(blocker["fibery/id"])

    while True:
        modified = False
        for task in tasks:
            hl = (half_life(deadline_half_lifes[task["fibery/id"]]))
            # print(hl, task)
            for blocker in task["user/Tasks"]:
                if deadline_half_lifes[blocker["fibery/id"]] > hl:
                    deadline_half_lifes[blocker["fibery/id"]] = hl
                    modified = True
        if not modified:
            break

    sys.stderr.write("Assigned deadlines\n")
    sys.stderr.flush()

    people_graph = Digraph(name="cluster_people")

    latest_task_of_user = {}

    # Priorities
    prioritized_tasks = [task['fibery/id'] for task in tasks if task['fibery/id'] not in hidden_tasks]
    prioritized_tasks.sort(key=lambda l: 
                               (
                               not(tasks_by_id[l]["Tasks/Commitment?"]),
                               #not(tasks_by_id[l]["Tasks/Has active goals?"]),
                               not (tasks_by_id[l]["__status"] == "In Progress" or tasks_by_id[l]["__status"] == "In Testing" or tasks_by_id[l]["__status"] == "To Test" or tasks_by_id[l]["__status"] == "Review"),    
                               min(tasks_by_id[l]["Priority"], 5),
                               tasks_by_id[l]["__sprint_end"],
                               #deadline_half_lifes[l],
                               -tasks_by_id[l]["ICE"],
                               -len(task["user/Tasks"]),
                               -len(tasks_by_id[l]["assignments/assignees"]),                               
                               -tasks_by_id[l]['Tasks/Estimate'],
                               int(tasks_by_id[l]['fibery/public-id'])
                               )
                           )
                               
    prioritized_tasks_copy = prioritized_tasks.copy()                               
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["user/project"].get("fibery/rank", -1) or -1)
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["ICE"])
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: -len(tasks_by_id[l]["assignments/assignees"]))
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: deadline_half_lifes[l])
    
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: -tasks_by_id[l]["ICE"])
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["__sprint_end"])
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["__status"] == "Backlog")
    #prioritized_tasks = sorted(prioritized_tasks, key=lambda l: min(tasks_by_id[l]["Priority"],5))
    #prioritized_tasks = sorted(prioritized_tasks,
                            #key=lambda l: tasks_by_id[l]["__status"] == "In Progress" or tasks_by_id[l][
                                #"__status"] == "In Testing" or tasks_by_id[l]["__status"] == "To Test" or tasks_by_id[l][
                                                #"__status"] == "Review", reverse=True)

    sys.stderr.write("Prioritized tasks\n")
    sys.stderr.flush()


    def date_hours_in_future(hours):
        weeks = int(hours / 40)
        hours = hours - weeks * 40
        days = int(hours / 8)
        hours = hours - days * 8
        sec_in_future = weeks * 7 * 24 * 3600 + days * 24 * 3600 + hours
        return (now + datetime.timedelta(0, sec_in_future)).strftime("%Y-%m-%d %H:%M:%S")






    
    # loop breaker. removes circular dependencies.
    prioritized_tasks_set = set(prioritized_tasks)
    while prioritized_tasks:
        for task_id in prioritized_tasks:
            task = tasks_by_id[task_id]
            is_blocked = any([t["fibery/id"] in prioritized_tasks_set for t in task["user/Tasks"]])
            if is_blocked:
                continue
            prioritized_tasks.remove(task_id)
            prioritized_tasks_set.remove(task_id)
            break
        else:
            # all tasks are blocked. remove one edge and try to align the rest of it.
            # first, try to remove an ephemeral implicit dependency
            for edge in ephemeral_dependencies:                
                if edge[0] in prioritized_tasks_set and edge[1] in prioritized_tasks_set:
                    tasks_by_id[edge[0]]["user/Tasks"] = [i for i in tasks_by_id[edge[0]]["user/Tasks"] if i["fibery/id"] != edge[1]]
                    ephemeral_dependencies.remove(edge)
                    sys.stderr.write("Removed ephemeral dependency %s - %s\n" % edge)
                    sys.stderr.flush()
                    break
            else:
                # there is no ephemeral dependencies creating a loop. there is a real one.
                # remove some dependencies from first element and try again.
                for dep in tasks_by_id[prioritized_tasks[0]]["user/Tasks"]:
                    fid = dep["fibery/id"]
                    if fid in prioritized_tasks_set:
                        tasks_by_id[prioritized_tasks[0]]["user/Tasks"] = [i for i in tasks_by_id[prioritized_tasks[0]]["user/Tasks"] if i["fibery/id"] != fid]
                        sys.stderr.write("Removed circular dependency %s - %s\n" % (prioritized_tasks[0], fid) )
                        sys.stderr.flush()                        
                        break
            
        
    
    
    
    
    
    
    
    prioritized_tasks = prioritized_tasks_copy
    prioritized_tasks_set = set(prioritized_tasks)
    max_user_time = {}
    for user in users:
        max_user_time[user] = 0


    blocked_users = set()
    task_end_times = {}
    task_end_hours = {}
    working_on_now = {}
    prioritized_tasks_set = set(prioritized_tasks)
    cur_task_rank = 0
    
    # every assignee looks for a task and picks it
    while prioritized_tasks and users:
        min_user = None
        min_user_time = 999999999999999999999999999

        # find not busy user
        for user in sorted(users):
            if user in blocked_users:
                continue
            if max_user_time[user] < min_user_time:
                min_user = user
                min_user_time = max_user_time[user]
        if not min_user:
            break
        # find non blocked job for user
        for task_id in prioritized_tasks:
            task = tasks_by_id[task_id]
            is_blocked = any([t["fibery/id"] in prioritized_tasks_set for t in task["user/Tasks"]])
            if is_blocked:
                continue
            assignees = [t["fibery/id"] for t in task["assignments/assignees"]]
 

            if min_user in assignees:
                blocked_users = set()
                prioritized_tasks.remove(task_id)
                prioritized_tasks_set.remove(task_id)
                min_free_all_users_time = min_user_time
                
                
                task["new_rank"] = cur_task_rank
                cur_task_rank += 1
                
                for assignee in assignees:
                    if max_user_time[assignee] > min_free_all_users_time:
                        min_free_all_users_time = max_user_time[assignee]
                for blocker in task["user/Tasks"]:
                    if blocker["fibery/id"] in task_end_hours:
                        if task_end_hours[blocker["fibery/id"]] > min_free_all_users_time:
                            min_free_all_users_time = task_end_hours[blocker["fibery/id"]]
                task_end_time = min_free_all_users_time + task['Tasks/Estimate']
                task_end_times[task_id] = date_hours_in_future(task_end_time)
                task_end_hours[task_id] = task_end_time
                for assignee in assignees:
                    max_user_time[assignee] = task_end_time
                task_short = {"name":task["Tasks/name"], "status": task["__status"], "type":task["__type"], "id":task['fibery/public-id'], 'started_at':task.get('Tasks/Actual~start'), 'will_fail': False}
                
                
                
                for assignee in task["assignments/assignees"]:
                    if assignee["fibery/id"] in latest_task_of_user:
                        # add intermediate edge to the workflow chart
                        dot.edge(latest_task_of_user[assignee["fibery/id"]], task["fibery/id"], color="orange",
                                weight="100")
                        
                        # will the task fail the time? mark to the short task
                        if task['Tasks/Deadline']:
                            if task["fibery/id"] in task_end_times:
                                if task['Tasks/Deadline'] < task_end_times[task["fibery/id"]]:
                                    task_short["will_fail"] = True
                        
                        # post about this task to json that gets posted to slack
                        if len(working_on_now[assignee["user/name"]]) < 3 or task["__status"] == "In Testing" or task["__status"] == "In Progress" or task["__status"] == "Review" or task["__status"] == "Buffering" or task["__status"] == "Analysis" or task_short["will_fail"]:
                            working_on_now[assignee["user/name"]].append(task_short)

                    else:
                        people_graph.node(assignee["fibery/id"], assignee["user/name"])
                        dot.edge(assignee["fibery/id"], task["fibery/id"], color="orange", weight="1000")
                        working_on_now[assignee["user/name"]] = [task_short]
                    latest_task_of_user[assignee["fibery/id"]] = task["fibery/id"]
                break
        else:
            blocked_users.add(min_user)
    open('unaligned_tasks.json', "w").write(json.dumps(prioritized_tasks))
    open('people_working_on.json','w').write(json.dumps(working_on_now))



    with open('tasknames.csv', 'w') as csvfile:
        namewriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for task in tasks:
            namewriter.writerow([task["fibery/id"], task["Tasks/name"], 'https://kontur.fibery.io/Tasks/%s/%s/edit' % (task["__type"], task['fibery/public-id']), task['__status'], task.get("new_rank", 0), task.get('fibery/rank', 0)]) 


#    open('all_tasks.json','w').write(json.dumps(tasks_by_id))

    sys.stderr.write("Created assignees tasks chain\n")
    sys.stderr.flush()



    people_graph.graph_attr["rank"] = "source"
    dot.subgraph(people_graph)


    sprints = {}
    task_ends = {}
    # sprints["no"] = Digraph(name="cluster_no_sprint")

    def break_task_name(name):
        num_chunks = int(len(name) / 35) + 1
        if num_chunks > 1:
            chunk_length = int(len(name) / num_chunks) + 1
            ns = name.split()
            groups = [""]
            for part in ns:
                groups[-1] += " "
                groups[-1] += part
                if len(groups[-1]) > chunk_length:
                    groups.append("")
            name = "\n".join(groups)
        return name
                

    for task in tasks:
        gr = dot
        # gr = sprints["no"]
        #subgraph_name = task['user/User Story'].get("Tasks/name")
        subgraph_name = task['user/Sprint'].get("Tasks/name")
        #subgraph_name = None
        
        if subgraph_name:
            if subgraph_name not in sprints:
                sprints[subgraph_name] = Digraph(
                    name="cluster_sprint_" + subgraph_name)
                sprints[subgraph_name].graph_attr["label"] = subgraph_name
            gr = sprints[subgraph_name]
        if task["fibery/id"] not in hidden_tasks:
            fillcolor = 'white'
            deadline = ""
            if task['Tasks/Deadline']:
                if task["fibery/id"] in task_end_times:
                    if task['Tasks/Deadline'] < task_end_times[task["fibery/id"]]:
                        fillcolor = 'red'
                deadline = " // deadline: " + task['Tasks/Deadline']

            color = 'black'
            if task["__status"] == "Done":
                color = 'green'
                if task["Tasks/Verified by QA"]:
                    fillcolor = 'green'

            if task["__status"] == "In Progress":
                color = 'orange'

            task_end = ""
            try:
                task_end = up_date(task_end_times[task["fibery/id"]])
            except:
                color = 'red'

            dot.node(task["fibery/id"],
                    '#' + task['fibery/public-id'] + "  " + str(
                        math.ceil(task["Tasks/Estimate"])) + "h  " + task_end + deadline + "\\l" + break_task_name(task[
                        "Tasks/name"]) + "\\n" + "".join(
                        [assignee["user/name"] + '\\r' for assignee in task["assignments/assignees"]]), color=color,
                    fillcolor=fillcolor, style='filled',
                    URL='https://kontur.fibery.io/Tasks/%s/%s/edit' % (task["__type"], task['fibery/public-id']))
            
            sprint_name = task['user/Sprint'].get("Tasks/name")
            if not sprint_name:
                sprint_name = ""
                
            if fillcolor == "red":
                task_end = 'cluster_fail_'
            task_end_cluster = task_end + '_' + sprint_name
            if task_end_cluster not in task_ends:
                task_ends[task_end_cluster] = set([task["fibery/id"]])
            else:
                task_ends[task_end_cluster].add(task["fibery/id"])
            
            for blocker in task["user/Tasks"]:
                if blocker["fibery/id"] not in hidden_tasks:
                    dot.edge(blocker["fibery/id"], task["fibery/id"],weight="1")
    
  #  for sprint in sprints.values():
  #      dot.subgraph(sprint)

    for task_end in sorted(task_ends.keys()):
        gr = Digraph(name= task_end)
        if "cluster" not in task_end:
            gr.attr(rank='same')
        for n in task_ends[task_end]:
            gr.node(n)
        dot.subgraph(gr)


    print(dot.source)

aaa()
