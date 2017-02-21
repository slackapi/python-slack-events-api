Example Slack events API bot
===================================

This example app shows how easy it is to implement the Slack Events API Adapter
to receive Slack Events, extend it to handle the OAuth flow and respond to
messages using Slack's Web API via python-slackclient.

🤖  Setup and running the app
------------

**Set up your Python environment:**

See `virtualenv`_ docs for more info.

.. _virtualenv: https://virtualenv.pypa.io

.. code::

  virtualenv -p /your/path/to/python2 env
  source env/bin/activate


**Install the app's dependencies:**

.. code::

  pip install -r requirements.txt

**🤖  Create a Slack app**

Create a Slack app on https://api.slack.com/apps/

.. image:: https://cloud.githubusercontent.com/assets/32463/20549718/afdd98d0-b0e3-11e6-8d83-8ad7053deb80.png

Add a **bot user** for your app

.. image:: https://cloud.githubusercontent.com/assets/32463/20371297/9044e2a0-ac18-11e6-8f25-3ffbd8a3bf58.png

**🤖  Run the app:**

You'll need to have your server and ngrok running to complete your app's Event
Subscription setup

.. code::

  python example.py

**🤖  Start ngrok**

In order for Slack to contact your local server, you'll need to run a tunnel. We
recommend ngrok or localtunnel. We're going to use ngrok for this example.

    💡  Slack requires event requests be delivered over SSL, so you'll want to
    use the HTTPS URL provided by ngrok.

Run ngrok and copy the **HTTPS** URL

.. code::

  ngrok http 3000

.. code::

  ngrok by @inconshreveable (Ctrl+C to quit)

  Session status                      online
  Version                             2.1.18
  Region                  United States (us)
  Web Interface        http://127.0.0.1:4040

  Forwarding http://h7465j.ngrok.io -> localhost:9292
  Forwarding https://h7465j.ngrok.io -> localhost:9292

**🤖  Subscribe your app to events**

Add your **Request URL** (your ngrok URL + ``/slack/events``) and subscribe your app to `message.channels` under bot events. **Save** and toggle **Enable Events** to `on`

.. image:: https://cloud.githubusercontent.com/assets/32463/20366593/b40d14a4-ac00-11e6-8413-b473c16ef997.png

.. image:: https://cloud.githubusercontent.com/assets/32463/20549612/e7ee2ed4-b0e2-11e6-8b9c-01ed08057c7c.png

**🤖  Save your app's credentials**

Go to your app's **Basic Information** page and save your app's **Client ID**, **Client Secret** and **Verification Token** to environmental variables

.. image:: https://cloud.githubusercontent.com/assets/32463/20445302/61ddfc54-ad89-11e6-8523-245a60c875b0.png

**🤖  Add your OAuth URL**

Add your OAuth redirect URL (your ngrok URL + ``/auth/slack/callback``)

.. image:: https://cloud.githubusercontent.com/assets/32463/20543629/63e41a26-b0bb-11e6-8eee-90c6f4f1dbb1.png

**🤖  Assign your app's credentials to environment variables:**

.. code::

  export SLACK_CLIENT_ID=xxxxxxxxxxx.xxxxxxxxxxxxx
  export SLACK_CLIENT_SECRET=XxxxXxxXXXxxXxxXX
  export SLACK_VERIFICATION_TOKEN=xxxxxxxxXxxXxxXxXXXxxXxxx

**🤖  Restart your app to load it's credentials**

.. code::

  python example.py


**🤖  Auth your app**

Go to your ngrok URL (e.g. https://myapp12.ngrok.com/) and auth your app.

.. image:: https://cloud.githubusercontent.com/assets/32463/20575277/789c0c5a-b16d-11e6-86fd-e30c3a0d2e61.gif

**🎉 Once your app has been authorized, you will begin receiving Slack events**

**👋🏻  Interact with your bot:**

Invite your bot to a public channel, then say hi and your bot will respond

    hi @bot 👋🏻

.. image:: https://cloud.githubusercontent.com/assets/32463/23047918/964defec-f467-11e6-87c3-9c7da11fc810.gif

🤔  Support
-------

Need help? Join `dev4slack`_ and talk to us in `#slack-api`_.

You can also `create an Issue`_ right here on GitHub.

.. _Events API: https://api.slack.com/events-api
.. _create a Slack App: https://api.slack.com/apps/new
.. _Event Subscriptions: https://api.slack.com/events-api#subscriptions
.. _dev4slack: http://dev4slack.xoxco.com/
.. _#slack-api: https://dev4slack.slack.com/messages/slack-api/
.. _create an Issue: https://github.com/slackapi/node-slack-events-api/issues/new
