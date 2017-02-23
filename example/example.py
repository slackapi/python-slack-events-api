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

# Since SlackEventAdapter uses a standard Flask server, we can extend it to handle OAuth
# by simply adding a couple more route handlers.

# Slack App credentials for OAuth
SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]


# This route renders the installation page with 'Add to Slack' button.
@slack_events_adapter.server.route("/", methods=["GET"])
def pre_install():
    add_to_slack = """
        <a href="https://slack.com/oauth/authorize?scope=bot&client_id=%s">
            <img alt="Add to Slack" src="https://platform.slack-edge.com/img/add_to_slack.png"/>
        </a>
    """ % SLACK_CLIENT_ID
    return add_to_slack


# This route is called by Slack after the user installs our app. It will
# exchange the temporary authorization code Slack sends for an OAuth token
# which we'll save on the bot object to use later.
# To let the user know what's happened it will also render a thank you page.
@slack_events_adapter.server.route("/auth/slack/callback", methods=["GET"])
def thanks():

    # Get the OAuth code to pass into the token request
    auth_code = request.args.get('code')

    # Create a temporary Slack client to make the OAuth request.
    # This client doesn't need a token.
    slack_client = SlackClient("")

    # Ask Slack for a bot token, using the auth code we received
    auth_response = slack_client.api_call(
        "oauth.access",
        client_id=SLACK_CLIENT_ID,
        client_secret=SLACK_CLIENT_SECRET,
        code=auth_code
    )

    # Grab the user's team info and token from the OAuth response
    team_id = auth_response.get("team_id")
    team_name = auth_response.get("team_name")
    bot_token = auth_response["bot"].get("bot_access_token")

    # Create a SlackClient for your bot to use for Web API requests
    CLIENTS[team_id] = SlackClient(bot_token)
    return "Your app has been installed on <b>%s</b>" % team_name


# Now we'll set up some event listeners for our app to process and respond to
# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    team_id = event_data["team_id"]
    message = event_data["event"]
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        CLIENTS[team_id].api_call("chat.postMessage", channel=channel, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    team_id = event_data["team_id"]
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    CLIENTS[team_id].api_call("chat.postMessage", channel=channel, text=text)


# Once we have our addon routes and event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
