import requests
import json
import sys
import dateutil.parser as dp
from graphviz import Digraph
from datetime import date
import datetime
import csv
import math
from config_loader import import_config
from log import get_logger
from queries import GET_TASKS_QUERY, GET_STORIES_QUERY
from fibery_api import command_result

TOKEN, FIBERY_BASE_URL = import_config("TOKEN", "FIBERY_BASE_URL")
log = get_logger(__name__)

now = datetime.datetime.now()

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
}

get_tasks_command = GET_TASKS_QUERY
get_stories_command = GET_STORIES_QUERY


json.loads(get_tasks_command)
r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=get_tasks_command, headers=headers)
tasks = command_result(r)
if tasks is None:
    sys.stderr.write(r.text)
sys.stderr.write("Got tasks\n")
sys.stderr.flush()


json.loads(get_stories_command)
r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=get_stories_command, headers=headers)
stories = command_result(r)
if stories is None:
    sys.stderr.write(r.text)
sys.stderr.write("Got user stories\n")
sys.stderr.flush()

tasks += stories

dot = Digraph()
dot.graph_attr["rankdir"] = "TB"
dot.graph_attr["newrank"] = "true"
# Increase graph complexity limits a bit
dot.graph_attr["nslimit"] = "10.0"
dot.graph_attr["nodesep"] = "1"
# dot.graph_attr["nslimit"] = "50.0"
# dot.graph_attr["concentrate"]="true"

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


# def tomorrow(d):
# return dp.parse(d) +i

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
    # Substories block their parent tasks
    if "user/Substories" in task:
        task["user/Tasks"].extend(task["user/Substories"])

    # Story subtasks block all tasks of the story
    if "user/User Story" in task:
        task["user/Tasks"].extend(task["user/User Story"].get("user/Substories", []))
        for story in task["user/User Story"].get("user/Substories", []):
            ephemeral_dependencies.add((task["fibery/id"], story["fibery/id"]))

    # Avoid self-dependencies accidentally introduced
    task["user/Tasks"] = [i for i in task["user/Tasks"] if i["fibery/id"] != task["fibery/id"]]
    if "Tasks/Deadline" not in task:  # US have no deadline
        task["Tasks/Deadline"] = None
        task["__type"] = "User_Story"
    if "user/Contract" not in task:
        task["user/Contract"] = {"Tasks/Deadline": None}
    if "Tasks/Verified by QA" not in task:
        task["Tasks/Verified by QA"] = True
    if "Tasks/Story Point float" not in task:
        task["Tasks/Story Point float"] = 0
    if "user/project" not in task:
        task["user/project"] = {}
    if "Tasks/Actual~Finish" not in task:
        task["Tasks/Actual~Finish"] = None

    if not task["Priority"]:
        task["Priority"] = 5  # 5 is Normal priority

    task["__sprint_end"] = "9999-12-30"
    if task["__status"] == "Backlog":
        hl = "9999-12-30"
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
    if task["__status"] == "Done":
        hidden_tasks.add(task["fibery/id"])
        skip_qa = True
    if task["__status"] == "Verified by QA":  # and task["Tasks/Verified by QA"]:
        hidden_tasks.add(task["fibery/id"])
    if not task["Tasks/name"]:
        task["Tasks/name"] = ""

    task['Tasks/Estimate'] = 8
    if task['Tasks/Story Point float']:
        # TODO: read Story Points
        #        if task['Tasks/Story Point float']:
        task['Tasks/Estimate'] = float(task['Tasks/Story Point float']) * 9

    task['Tasks/Estimate'] = float(task['Tasks/Estimate'])

    if "workflow/state" in task["user/Contract"]:
        if task["user/Contract"]["workflow/state"]["enum/name"] in ["Stopped", "Done"]:
            hidden_tasks.add(task["fibery/id"])
            skip_qa = True

    if "workflow/state" in task["user/project"]:
        if task["user/project"]["workflow/state"]["enum/name"] in ["Stopped", "Done"]:
            hidden_tasks.add(task["fibery/id"])
            skip_qa = True

    if "Yannick" in task["Tasks/name"]:
        task["assignments/assignees"] = [assignee for assignee in task["assignments/assignees"] if
                                         assignee['user/name'] != 'Darafei Praliaskouski']
        task["assignments/assignees"].append({'fibery/id': 'Yannick', 'user/name': 'Yannick Guenet'})
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
        t['Tasks/Estimate'] = t['Tasks/Estimate'] / 2
        t["assignments/assignees"] = [
            {'fibery/id': '455f2f50-5627-11e9-bcdd-8aba22381101', 'user/name': 'Anastasiya Zhdanovskaya'},
            {'fibery/id': 'b85ccda0-6373-11ea-8da1-c73fee560e63', 'user/name': 'Pavel Rytvinsky'}]
        t["user/Tasks"] = [{"fibery/id": task["fibery/id"]}]
        qa_tasks.append(t)
        deadline_half_lifes[t["fibery/id"]] = hl

tasks += qa_tasks

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
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["user/project"].get("fibery/rank", -1) or -1)
#prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["ICE"])
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: -tasks_by_id[l]["ICE"])
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: deadline_half_lifes[l])
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["__sprint_end"])
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["__status"] == "Backlog")
prioritized_tasks = sorted(prioritized_tasks, key=lambda l: tasks_by_id[l]["Priority"])
prioritized_tasks = sorted(prioritized_tasks,
                           key=lambda l: tasks_by_id[l]["__status"] == "In Progress" or tasks_by_id[l][
                               "__status"] == "In Testing" or tasks_by_id[l]["__status"] == "To Test" or tasks_by_id[l][
                                             "__status"] == "Review", reverse=True)

prioritized_tasks_copy = prioritized_tasks.copy()

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
        removed = False
        for edge in list(ephemeral_dependencies):
            if edge[0] in prioritized_tasks_set and edge[1] in prioritized_tasks_set:
                tasks_by_id[edge[0]]["user/Tasks"] = [i for i in tasks_by_id[edge[0]]["user/Tasks"] if i["fibery/id"] != edge[1]]
                ephemeral_dependencies.remove(edge)
                sys.stderr.write(f"Removed ephemeral dependency {edge[0]} - {edge[1]}\n")
                sys.stderr.flush()
                removed = True
                break
        if not removed:
            for dep in tasks_by_id[prioritized_tasks[0]]["user/Tasks"]:
                fid = dep["fibery/id"]
                if fid in prioritized_tasks_set:
                    tasks_by_id[prioritized_tasks[0]]["user/Tasks"] = [i for i in tasks_by_id[prioritized_tasks[0]]["user/Tasks"] if i["fibery/id"] != fid]
                    sys.stderr.write(f"Removed circular dependency {prioritized_tasks[0]} - {fid}\n")
                    sys.stderr.flush()
                    break
        prioritized_tasks = prioritized_tasks_copy
        prioritized_tasks_set = set(prioritized_tasks)

sys.stderr.write("Prioritized tasks\n")
sys.stderr.flush()

max_user_time = {}
for user in users:
    max_user_time[user] = 0


def date_hours_in_future(hours):
    weeks = int(hours / 40)
    hours = hours - weeks * 40
    days = int(hours / 8)
    hours = hours - days * 8
    sec_in_future = weeks * 7 * 24 * 3600 + days * 24 * 3600 + hours
    return (now + datetime.timedelta(0, sec_in_future)).strftime("%Y-%m-%d %H:%M:%S")


blocked_users = set()
task_end_times = {}
task_end_hours = {}
working_on_now = {}
while prioritized_tasks and users:
    min_user = None
    min_user_time = 999999999999999999999999999

    # find not busy user
    for user in users:
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
        is_blocked = any([t["fibery/id"] in prioritized_tasks for t in task["user/Tasks"]])
        if is_blocked:
            continue
        assignees = [t["fibery/id"] for t in task["assignments/assignees"]]

        if min_user in assignees:
            blocked_users = set()
            prioritized_tasks.remove(task_id)
            min_free_all_users_time = min_user_time
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
            task_short = {"name":task["Tasks/name"], "status": task["__status"], "type":task["__type"], "id":task['fibery/public-id']}
            for assignee in task["assignments/assignees"]:
                if assignee["fibery/id"] in latest_task_of_user:
                    dot.edge(latest_task_of_user[assignee["fibery/id"]], task["fibery/id"], color="orange",
                             weight="1000")
                    if len(working_on_now[assignee["user/name"]]) < 3 or task["__status"] == "In Testing" or task["__status"] == "In Progress" or task["__status"] == "Review":
                        working_on_now[assignee["user/name"]].append(task_short)

                else:
                    people_graph.node(assignee["fibery/id"], assignee["user/name"])
                    dot.edge(assignee["fibery/id"], task["fibery/id"], color="orange", weight="1000")
                    working_on_now[assignee["user/name"]] = [task_short]
                latest_task_of_user[assignee["fibery/id"]] = task["fibery/id"]
            break
    else:
        blocked_users.add(min_user)
open('unaligned_tasks.json', 'w').write(json.dumps(prioritized_tasks))
open('people_working_on.json','w').write(json.dumps(working_on_now))

with open('tasknames.csv', 'w', newline='') as csvfile:
    namewriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for task in tasks:
        namewriter.writerow([
            task["fibery/id"],
            task["Tasks/name"],
            f"{FIBERY_BASE_URL}/Tasks/{task['__type']}/{task['fibery/public-id']}/edit",
            task['__status'],
            task.get("new_rank", 0),
            task.get('fibery/rank', 0),
        ])

people_graph.graph_attr["rank"] = "source"
dot.subgraph(people_graph)


sprints = {}
# sprints["no"] = Digraph(name="cluster_no_sprint")

for task in tasks:
    gr = dot
    # gr = sprints["no"]
    if task['user/Sprint']["Tasks/name"]:
        if task['user/Sprint']["Tasks/name"] not in sprints:
            sprints[task['user/Sprint']["Tasks/name"]] = Digraph(
                name="cluster_sprint_" + task['user/Sprint']["Tasks/name"])
            sprints[task['user/Sprint']["Tasks/name"]].graph_attr["label"] = task['user/Sprint']["Tasks/name"]
        gr = sprints[task['user/Sprint']["Tasks/name"]]
    if task["fibery/id"] not in hidden_tasks:
        fillcolor = 'white'
        deadline = ""
        if task['Tasks/Deadline']:
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

        gr.node(task["fibery/id"],
                '#' + task['fibery/public-id'] + "  " + str(
                    math.ceil(task["Tasks/Estimate"])) + "h  " + task_end + deadline + "\\l" + task[
                    "Tasks/name"] + "\\n" + "".join(
                    [assignee["user/name"] + '\\r' for assignee in task["assignments/assignees"]]), color=color,
                fillcolor=fillcolor, style='filled',
                URL=f"{FIBERY_BASE_URL}/Tasks/%s/%s/edit" % (task["__type"], task['fibery/public-id']))

        for blocker in task["user/Tasks"]:
            if blocker["fibery/id"] not in hidden_tasks:
                dot.edge(blocker["fibery/id"], task["fibery/id"])

for sprint in sprints.values():
    dot.subgraph(sprint)

log.info(dot.source)
