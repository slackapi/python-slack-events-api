Slack Events API adapter for Python
===================================

.. image:: https://badge.fury.io/py/slackeventsapi.svg
  :target: https://pypi.org/project/slackeventsapi/
.. image:: https://travis-ci.org/slackapi/python-slack-events-api.svg?branch=main
  :target: https://travis-ci.org/slackapi/python-slack-events-api
.. image:: https://codecov.io/gh/slackapi/python-slack-events-api/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/slackapi/python-slack-events-api


The Slack Events Adapter is a Python-based solution to receive and parse events
from Slack’s Events API. This library uses an event emitter framework to allow
you to easily process Slack events by simply attaching functions
to event listeners.

This adapter enhances and simplifies Slack's Events API by incorporating useful best practices, patterns, and opportunities to abstract out common tasks.

💡  We wrote a `blog post which explains how`_ the Events API can help you, why we built these tools, and how you can use them to build production-ready Slack apps.

.. _blog post which explains how: https://medium.com/@SlackAPI/enhancing-slacks-events-api-7535827829ab

⚠️  Important Notice
---------------------

If you use this library for Events API handling, you may need to use threads for stable event acknowledgement. See https://github.com/slackapi/python-slack-events-api/issues/84 for details.

If you're looking for the best recommended library at this point, check Bolt for Python: https://github.com/slackapi/bolt-python

The framework covers not only Events API but also all the latest Slack Platform features.

🤖  Installation
----------------

.. code:: shell

  pip install slackeventsapi

🤖  App Setup
--------------------

Before you can use the `Events API`_ you must
`create a Slack App`_, and turn on
`Event Subscriptions`_.

💡  When you add the Request URL to your app's Event Subscription settings,
Slack will send a request containing a `challenge` code to verify that your
server is alive. This package handles that URL Verification event for you, so
all you need to do is start the example app, start ngrok and configure your
URL accordingly.

✅  Once you have your `Request URL` verified, your app is ready to start
receiving Team Events.

🔑  Your server will begin receiving Events from Slack's Events API as soon as a
user has authorized your app.

🤖  Development workflow:
===========================

(1) Create a Slack app on https://api.slack.com/apps
(2) Add a `bot user` for your app
(3) Start the example app on your **Request URL** endpoint
(4) Start ngrok and copy the **HTTPS** URL
(5) Add your **Request URL** and subscribe your app to events
(6) Go to your ngrok URL (e.g. https://myapp12.ngrok.com/) and auth your app

**🎉 Once your app has been authorized, you will begin receiving Slack Events**

    ⚠️  Ngrok is a great tool for developing Slack apps, but we don't recommend using ngrok
    for production apps.

🤖  Usage
----------
  **⚠️  Keep your app's credentials safe!**

  - For development, keep them in virtualenv variables.

  - For production, use a secure data store.

  - Never post your app's credentials to github.

.. code:: python

  SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

Create a Slack Event Adapter for receiving actions via the Events API
-----------------------------------------------------------------------
**Using the built-in Flask server:**

.. code:: python

  from slackeventsapi import SlackEventAdapter


  slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")


  # Create an event listener for "reaction_added" events and print the emoji name
  @slack_events_adapter.on("reaction_added")
  def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(emoji)


  # Start the server on port 3000
  slack_events_adapter.start(port=3000)


**Using your existing Flask instance:**


.. code:: python

  from flask import Flask
  from slackeventsapi import SlackEventAdapter


  # This `app` represents your existing Flask app
  app = Flask(__name__)


  # An example of one of your Flask app's routes
  @app.route("/")
  def hello():
    return "Hello there!"


  # Bind the Events API route to your existing Flask app by passing the server
  # instance as the last param, or with `server=app`.
  slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


  # Create an event listener for "reaction_added" events and print the emoji name
  @slack_events_adapter.on("reaction_added")
  def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(emoji)


  # Start the server on port 3000
  if __name__ == "__main__":
    app.run(port=3000)

For a comprehensive list of available Slack `Events` and more information on
`Scopes`, see https://api.slack.com/events-api

🤖  Example event listeners
-----------------------------

See `example.py`_ for usage examples. This example also utilizes the
SlackClient Web API client.

.. _example.py: /example/

🤔  Support
-----------

Need help? Join `Slack Community`_ and talk to us in `#slack-api`_.

You can also `create an Issue`_ right here on GitHub.

.. _Events API: https://api.slack.com/events-api
.. _create a Slack App: https://api.slack.com/apps/new
.. _Event Subscriptions: https://api.slack.com/events-api#subscriptions
.. _Slack Community: http://slackcommunity.com/
.. _#slack-api: https://dev4slack.slack.com/messages/slack-api/
.. _create an Issue: https://github.com/slackapi/python-slack-events-api/issues/new
