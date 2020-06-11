Example Slack events API bot
=============================

This example app shows how easy it is to implement the Slack Events API Adapter
to receive Slack Events and respond to
messages using Slack's Web API via python-slackclient.

🤖  Setup and running the app
------------------------------

**Set up your Python environment:**

We're using virtualenv to keep the dependencies and environmental variables specific to this app. See `virtualenv`_ docs for more info.

.. _virtualenv: https://virtualenv.pypa.io

This example app works best in Python 2.7. If 2.7 is your default version, create a virtual environment by running:

.. code::

  virtualenv env

Otherwise, if Python 3+ is your default, specify the path to your 2.7 instance:

.. code::

  virtualenv -p /your/path/to/python2 env

Then initialize the virtualenv:

.. code::

  source env/bin/activate


**Install the app's dependencies:**

.. code::

  pip install -r requirements.txt

**🤖  Create a Slack app**

Create a Slack app on https://api.slack.com/apps/

.. image:: https://cloud.githubusercontent.com/assets/32463/24877733/32979776-1de5-11e7-87d4-b5dc9e3e7973.png

**🤖  Add a bot user to your app**

.. image:: https://cloud.githubusercontent.com/assets/32463/24877750/47a16034-1de5-11e7-989b-2a90b9d8e7e3.png

**🤖  Install your app on your team**

Visit your app's **Install App** page and click **Install App to Team**.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877770/61804c36-1de5-11e7-91ef-5cf2e0845729.png

Authorize your app

.. image:: https://cloud.githubusercontent.com/assets/32463/24877792/774ed94c-1de5-11e7-8857-ac8d662c5b27.png

**🤖  Save your app's credentials**

Once you've authorized your app, you'll be presented with your app's tokens.

.. image:: https://cloud.githubusercontent.com/assets/32463/24877652/d8eebbb4-1de4-11e7-8f75-2cfb1e9d45ee.png

Copy your app's **Bot User OAuth Access Token** and add it to your python environmental variables

.. code::

  export SLACK_BOT_TOKEN=xxxXXxxXXxXXxXXXXxxxX.xXxxxXxxxx

Next, go back to your app's **Basic Information** page

.. image:: https://user-images.githubusercontent.com/32463/43932347-63b21eca-9bf8-11e8-8b30-0a848c263bb1.png

Add your app's **Signing Secret** to your python environmental variables

.. code::

  export SLACK_SIGNING_SECRET=xxxxxxxxXxxXxxXxXXXxxXxxx


**🤖  Start ngrok**

In order for Slack to contact your local server, you'll need to run a tunnel. We
recommend ngrok or localtunnel. We're going to use ngrok for this example.

If you don't have ngrok, `download it here`_.

.. _download it here: https://ngrok.com


Here's a rudimentary diagream of how ngrok allows Slack to connect to your server

.. image:: https://cloud.githubusercontent.com/assets/32463/25376866/940435fa-299d-11e7-9ee3-08d9427417f6.png


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

**🤖  Run the app:**

You'll need to have your server and ngrok running to complete your app's Event
Subscription setup

.. code::

  python example.py


**🤖  Subscribe your app to events**

Add your **Request URL** (your ngrok URL + ``/slack/events``) and subscribe your app to `message.channels` under bot events. **Save** and toggle **Enable Events** to `on`

.. image:: https://user-images.githubusercontent.com/1573454/30185162-644d0cb8-93ee-11e7-96af-55fe10d9d5c8.png

.. image:: https://cloud.githubusercontent.com/assets/32463/24877931/e119181a-1de5-11e7-8b0c-fcbc3419bad7.png

**🎉  Once your app has been installed and subscribed to Bot Events, you will begin receiving event data from Slack**

**👋  Interact with your bot:**

Invite your bot to a public channel, then say hi and your bot will respond

    hi @bot 👋

.. image:: https://cloud.githubusercontent.com/assets/32463/23047918/964defec-f467-11e6-87c3-9c7da11fc810.gif

🤔  Support
------------

Need help? Join `Bot Developer Hangout`_ and talk to us in `#slack-api`_.

You can also `create an Issue`_ right here on GitHub.

.. _Bot Developer Hangout: http://dev4slack.xoxco.com/
.. _#slack-api: https://dev4slack.slack.com/messages/slack-api/
.. _create an Issue: https://github.com/slackapi/node-slack-events-api/issues/new
