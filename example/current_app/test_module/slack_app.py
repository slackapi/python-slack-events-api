from flask import current_app as app
from slackeventsapi import SlackEventAdapter
import os

slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)
