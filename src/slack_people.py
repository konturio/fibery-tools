"""Send individual task updates to each Slack user."""

from log import get_logger

log = get_logger(__name__)
import dateutil.parser as dp
from datetime import date
import datetime
from slack import WebClient
from slack.errors import SlackApiError
from config_loader import import_config

SLACK_TOKEN, SLACK_CHANNEL, FIBERY_BASE_URL = import_config(
    "SLACK_TOKEN", "SLACK_CHANNEL", "FIBERY_BASE_URL"
)

client = WebClient(token=SLACK_TOKEN)
import json

def main() -> None:
    """Send every user their current tasks via Slack."""
    status = json.loads(open("people_working_on.json").read())

    for user in sorted(status.keys()):
        text = ""
        text += f"\n*{user}*\n"
        for task in status[user]:
            ago = ""
            if task["started_at"]:
                ago = "(started %s ago)" % (
                    ("%s" % (datetime.datetime.utcnow() - dp.parse(task["started_at"].split('Z')[0]))).split(",")[0]
                )
            will_fail = ""
            if task["will_fail"]:
                will_fail = "*scheduled to fail*"
            text += " *[%s]* %s <%s/Tasks/%s/%s|%s> %s %s \n" % (
                task["id"],
                task["status"],
                FIBERY_BASE_URL,
                task["type"],
                task["id"],
                task["name"].replace('>', '-'),
                will_fail,
                ago,
            )

        try:
            log.info(text)
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
