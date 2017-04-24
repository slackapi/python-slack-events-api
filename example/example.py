from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from flask import request
import os

# We'll store the SlackClient instances for each team in a
# dictionary, so we can have multiple teams authed
CLIENTS = {}

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Slack App credentials for OAuth
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Create a SlackClient for your bot to use for Web API requests
CLIENT = SlackClient(SLACK_BOT_TOKEN)


# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        CLIENT.api_call("chat.postMessage", channel=channel, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    CLIENT.api_call("chat.postMessage", channel=channel, text=text)

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
