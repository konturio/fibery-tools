import requests
import json
import sys
import dateutil.parser as dp
from graphviz import Digraph
from datetime import date
import datetime
import math
import csv
from config_loader import import_config
from log import get_logger
from fibery_api import command_result

TOKEN, FIBERY_BASE_URL = import_config("TOKEN", "FIBERY_BASE_URL")
log = get_logger(__name__)

def aaa():

    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "user flow charting reader",
    }

    get_steps_command = """
[
    {
        "command": "fibery.entity/query",
        "args": {
        "query": {
            "q/from": "Product management/Scenario Step",
            "q/select": {
                        "Name": [
                "Product management/Name"
            ],
            "rank": [
                    "fibery/rank"
            ],
            "creation-date": [
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
            "Product management/Scenario Steps After": {
                "q/from": [
                "Product management/Scenario Steps After"
                ], "q/select": {
                "fibery/id": [
                    "fibery/id" 
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
            
            },
            "q/offset": 0,
            "q/limit": "q/no-limit"
        },
        "params": {}
     }   
    }
]"""


    json.loads(get_steps_command)
    r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=get_steps_command, headers=headers)
    steps = command_result(r)
    if steps is None:
        log.warning("No steps returned")
        sys.stderr.write(r.text)
        steps = []

    log.info("Got steps")
    

    get_cases_command = """
[
    {
        "command": "fibery.entity/query",
        "args": {
        "query": {
            "q/from": "Product management/Use case",
            "q/select": {
                        "Name": [
                "Product management/name"
            ],
            "rank": [
                    "fibery/rank"
            ],
            "creation-date": [
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
            "Product management/Scenario Steps": {
                "q/from": [
                "Product management/Scenario Steps"
                ], "q/select": {
                "fibery/id": [
                    "fibery/id" 
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
            
            },
            "q/offset": 0,
            "q/limit": "q/no-limit"
        },
        "params": {}
     }   
    }
]"""


    json.loads(get_cases_command)
    r = requests.post(f"{FIBERY_BASE_URL}/api/commands", data=get_cases_command, headers=headers)
    cases = command_result(r)
    if cases is None:
        log.warning("No cases returned")
        sys.stderr.write(r.text)
        cases = []

    sys.stderr.write(r.text)
    log.info("Got cases")

    dot = Digraph()
    #dot.graph_attr["rankdir"] = "TB"
    dot.graph_attr["rankdir"] = "LR"
    dot.graph_attr["newrank"] = "true"
    #dot.graph_attr["nslimit"] = "10.0"
    #dot.graph_attr["nslimit1"] = "10.0"
    #dot.graph_attr["nodesep"] = "0.5"
    dot.graph_attr["nodesep"] = "1"
    dot.graph_attr["TBbalance"] = "min"

    # dot.graph_attr["nslimit"] = "50.0"
    #dot.graph_attr["concentrate"]="true"

    estimates = []

    dot.attr('node', shape='box')


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
    
    # generate case edges set
    case_edges = set()    
    for case in cases:
        for next_step in case["Product management/Scenario Steps"]:
            case_edges.add((case["fibery/id"], next_step["fibery/id"]))
        
    # generate step -> cases mapping
    cases_by_step = {}
    for case in cases:
        for next_step in case["Product management/Scenario Steps"]:
            if next_step["fibery/id"] not in cases_by_step:
                cases_by_step[next_step["fibery/id"]] = set()
            cases_by_step[next_step["fibery/id"]].add(case["fibery/id"])        
        
    hidden_case_edges = set()
    for step in steps:    
        color = 'black'
        fillcolor='white'

        dot.node(step["fibery/id"],
                    'Step #' + step['fibery/public-id'] + "\\l" + break_task_name(step[
                        "Name"]), color=color,
                    fillcolor=fillcolor, style='filled',
                    URL=f"{FIBERY_BASE_URL}/Product_management/Scenario_Step/%s/edit" % (step['fibery/public-id']))
        for next_step in step["Product management/Scenario Steps After"]:
            # need to decide on color. 
            # orange - if we replaced the direct edge from use case to this orange
            if cases_by_step.get(step["fibery/id"], set()).isdisjoint(cases_by_step.get(next_step["fibery/id"],set())):
                # sets are disjoint, edge is red and weak
                dot.edge(step["fibery/id"], next_step["fibery/id"], color="red", weight="1")
            else:
                # sets are adjacent. need to drop case edge to parent and add strong orange edge.
                for parent_case in cases_by_step.get(step["fibery/id"], set()).intersection(cases_by_step.get(next_step["fibery/id"],set())):
                    hidden_case_edges.add((parent_case, next_step["fibery/id"]))
                    
                dot.edge(step["fibery/id"], next_step["fibery/id"], color="orange", weight="1000")

    gr = Digraph()
    gr.attr(rank='same')
    for case in cases:
        color = 'orange'
        fillcolor='white'
        gr.node(case["fibery/id"],
                    'Case #' + case['fibery/public-id'] + "\\l" + break_task_name(case[
                        "Name"]), color=color,
                    fillcolor=fillcolor, style='filled',
                    URL=f"{FIBERY_BASE_URL}/Product_management/Use_case/%s/edit" % (case['fibery/public-id']))
    dot.subgraph(gr)
    for case_edge in (case_edges-hidden_case_edges):
        dot.edge(case_edge[0], case_edge[1], color="orange", weight="1000")        



    log.info(dot.source)

aaa()
