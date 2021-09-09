import os
from slackeventsapi import SlackEventAdapter

slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

@slack_events_adapter.on("link_shared")
def handle_message(event_data):
    event = event_data["event"]
    print(f"event: {event}")

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

if __name__ == '__main__':
    slack_events_adapter.start(port=3000)

# -------------------------------

# (Terminal A)
# source env/bin/activate
# (env) $ export SLACK_SIGNING_SECRET=**
# (env) $ FLASK_ENV=development python example/issues/issue_49_link_shared_ampersand/example.py

# (Terminal B)
# ngrok http 3000

# in Slack
# /invite @{your app's bot user}
# share a URL "https://www.example.com/?foo=bar&baz=123"