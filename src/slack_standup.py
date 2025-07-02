"""Send a summary of ongoing work to Slack."""

from log import get_logger

log = get_logger(__name__)

from slack import WebClient
from slack.errors import SlackApiError
from config_loader import import_config

SLACK_TOKEN, SLACK_CHANNEL, FIBERY_BASE_URL = import_config(
    "SLACK_TOKEN", "SLACK_CHANNEL", "FIBERY_BASE_URL"
)

client = WebClient(token=SLACK_TOKEN)

import json

def main() -> None:
    """Post standup information to Slack."""
    status = json.loads(open("people_working_on.json").read())

    text = ""
    for user in sorted(status.keys()):
        text += f"\n*{user}*\n"
        for task in status[user]:
            text += " *[%s]* %s <%s/Tasks/%s/%s|%s> \n" % (
                task["id"],
                task["status"],
                FIBERY_BASE_URL,
                task["type"],
                task["id"],
                task["name"],
            )

    log.info(text)
    log.info(status)
    try:
        client.chat_postMessage(
            icon_emoji=":cat:",
            username="What's going on?",
            channel=SLACK_CHANNEL,
            text=text,
            type="mrkdwn",
        )
    except SlackApiError as e:
        assert e.response["error"]


if __name__ == "__main__":
    main()
