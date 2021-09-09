import os
from slack_sdk.web import WebClient
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask

app = Flask(__name__)

with app.app_context():
    from test_module.slack_app import slack_events_adapter

    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
    slack_client = WebClient(slack_bot_token)


    @slack_events_adapter.on("message")
    def handle_message(event_data):
        message = event_data["event"]
        if message.get("subtype") is None and "hi" in message.get('text'):
            channel = message["channel"]
            message = "Hi <@%s>! :tada:" % message["user"]
            slack_client.chat_postMessage(channel=channel, text=message)


    @slack_events_adapter.on("error")
    def error_handler(err):
        print("ERROR: " + str(err))

# (Terminal A)
# source env/bin/activate
# (env) $ export SLACK_BOT_TOKEN=xoxb-***
# (env) $ export SLACK_SIGNING_SECRET=**
# (env) $ cd example/current_app
# (env) $ FLASK_APP=main.py FLASK_ENV=development flask run --port 3000

# (Terminal B)
# ngrok http 3000

# in Slack
# /invite @{your app's bot user}
# post a message "hi" in the channel
