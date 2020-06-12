# ------------------
# Only for running this script here
import logging
import sys
from os.path import dirname

sys.path.insert(1, f"{dirname(__file__)}/../..")
logging.basicConfig(level=logging.DEBUG)
# ------------------

from slackeventsapi import SlackEventAdapter
from slack import WebClient
import os

slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# pip install proxy.py
# proxy --port 9000 --log-level d
proxy_info = "http://localhost:9000"
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=slack_bot_token, proxy=proxy_info)

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.chat_postMessage(channel=channel, text=message)


@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.chat_postMessage(channel=channel, text=text)

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

if __name__ == '__main__':
    slack_events_adapter.start(port=3000)

# -------------------------------

# (Terminal A)
# source env/bin/activate
# (env) $ export SLACK_BOT_TOKEN=xoxb-***
# (env) $ export SLACK_SIGNING_SECRET=**
# (env) $ FLASK_ENV=development python example/working_with_proxy/example.py

# (Terminal B)
# source env/bin/activate
# (env) $ proxy --port 9000 --log-level d

# (Terminal C)
# ngrok http 3000

# in Slack
# /invite @{your app's bot user}
# post a message "hi" in the channel