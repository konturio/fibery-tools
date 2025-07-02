"""Query templates used by workflow module."""

GET_TASKS_QUERY = r"""
  [
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
          "Tasks/Deadline": [
            "Tasks/Deadline"
          ],
          "Tasks/Verified by QA": [
            "Tasks/Verified by QA"
          ],
          "Tasks/Story Point float": [
            "Tasks/Story Point float"
          ],
          "Tasks/Skip QA": [
            "Tasks/Skip QA"
          ],
          "Tasks/name": [
            "Tasks/name"
          ],
          "__status": [
            "workflow/state",
            "enum/name"
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
            "Tasks/name": [
              "user/Contract",
              "Tasks/name"
            ],
            "Tasks/Deadline": [
              "user/Contract",
              "Tasks/Deadline"
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
          }          
        },
        "q/offset": 0,
        "q/limit": "q/no-limit"
      },
      "params": {}
    }
  }
  ]
"""

GET_STORIES_QUERY = r"""
  [
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
  ]
"""
