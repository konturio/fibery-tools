import logging
logging.basicConfig(level=logging.DEBUG)

from slack import WebClient
from slack.errors import SlackApiError
from config_loader import import_config

SLACK_TOKEN, SLACK_CHANNEL, FIBERY_BASE_URL = import_config(
    "SLACK_TOKEN", "SLACK_CHANNEL", "FIBERY_BASE_URL"
)

client = WebClient(token=SLACK_TOKEN)

import json

status = json.loads(open("people_working_on.json").read())

text = ""
for user in sorted(status.keys()):
    text += "\n*%s*\n"%user
    for task in status[user]:
        text += " *[%s]* %s <%s/Tasks/%s/%s|%s> \n" % (
            task["id"],
            task["status"],
            FIBERY_BASE_URL,
            task["type"],
            task["id"],
            task["name"],
        )
    

print(text)
print(status)
##exit()
try:
  response = client.chat_postMessage(
    icon_emoji=":cat:",
    username="What's going on?",
    channel=SLACK_CHANNEL,
    text=text,
    type="mrkdwn",
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
