import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

slack_token = "---getyourown-------------"
#slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

import json

status = json.loads(open("people_working_on.json").read())

text = ""
for user in sorted(status.keys()):
    text += "\n*%s*\n"%user
    for task in status[user]:
        text += " *[%s]* %s <https://kontur.fibery.io/Tasks/%s/%s|%s> \n" % (task["id"], task["status"], task["type"], task["id"], task["name"])
    

print(text)
print(status)
##exit()
try:
  response = client.chat_postMessage(
    icon_emoji=":cat:",
    username="What's going on?",
    channel="geocint",
    text=text,
    type="mrkdwn"
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
