import json
from flask import Flask
import pytest
import sys
import hmac
import time
from slackeventsapi import SlackEventAdapter
from slackeventsapi.server import SlackEventAdapterException
from slackeventsapi.version import __version__


def test_existing_flask():
    valid_flask = Flask(__name__)
    valid_adapter = SlackEventAdapter("SIGNING_SECRET", "/slack/events", valid_flask)
    assert isinstance(valid_adapter, SlackEventAdapter)


def test_server_not_flask():
    with pytest.raises(TypeError) as e:
        invalid_flask = "I am not a Flask"
        SlackEventAdapter("SIGNING_SECRET", "/slack/events", invalid_flask)
    assert e.value.args[0] == 'Server must be an instance of Flask'


def test_event_endpoint_get(client):
    # GET on '/slack/events' should 404
    res = client.get('/slack/events')
    assert res.status_code == 404


def test_url_challenge(client):
    slack_adapter = SlackEventAdapter("SIGNING_SECRET")
    data = pytest.url_challenge_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature(slack_adapter.signing_secret, timestamp, data)

    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json',
        headers={
            'X-Slack-Request-Timestamp': timestamp,
            'X-Slack-Signature': signature
        }
    )
    assert res.status_code == 200
    assert bytes.decode(res.data) == "valid_challenge_token"


def test_invalid_request_signature(client):
    # Verify [package metadata header is set
    slack_adapter = SlackEventAdapter("SIGNING_SECRET")

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = "bad signature"

    with pytest.raises(SlackEventAdapterException) as excinfo:
        res = client.post(
            '/slack/events',
            data=data,
            content_type='application/json',
            headers={
                'X-Slack-Request-Timestamp': timestamp,
                'X-Slack-Signature': signature
            }
        )

    assert str(excinfo.value) == 'Invalid request signature'


def test_invalid_request_timestamp(client):
    # Verify [package metadata header is set
    slack_adapter = SlackEventAdapter("SIGNING_SECRET")

    data = pytest.reaction_event_fixture
    timestamp = int(time.time()+1000)
    signature = "bad timestamp"

    with pytest.raises(SlackEventAdapterException) as excinfo:
        res = client.post(
            '/slack/events',
            data=data,
            content_type='application/json',
            headers={
                'X-Slack-Request-Timestamp': timestamp,
                'X-Slack-Signature': signature
            }
        )

    assert str(excinfo.value) == 'Invalid request timestamp'


def test_compare_digest_fallback(client, monkeypatch):
    # Verify [package metadata header is set
    slack_adapter = SlackEventAdapter("SIGNING_SECRET")

    if hasattr(hmac, "compare_digest"):
        monkeypatch.delattr(hmac, 'compare_digest')

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature =pytest.create_signature(slack_adapter.signing_secret, timestamp, data)

    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json',
        headers={
            'X-Slack-Request-Timestamp': timestamp,
            'X-Slack-Signature': signature
        }
    )

    assert res.status_code == 200


def test_version_header(client):
    # Verify [package metadata header is set
    slack_adapter = SlackEventAdapter("SIGNING_SECRET")
    package_info = slack_adapter.server.package_info

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature(slack_adapter.signing_secret, timestamp, data)

    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json',
        headers={
            'X-Slack-Request-Timestamp': timestamp,
            'X-Slack-Signature': signature
        }
    )

    assert res.status_code == 200
    assert res.headers["X-Slack-Powered-By"] == package_info


def test_server_start(mocker):
    # Verify server started with correct params
    slack_events_adapter = SlackEventAdapter("SIGNING_SECRET")
    mocker.spy(slack_events_adapter, 'server')
    slack_events_adapter.start(port=3000)
    slack_events_adapter.server.run.assert_called_once_with(debug=False, host='127.0.0.1', port=3000)


def test_default_exception_msg(mocker):
    with pytest.raises(SlackEventAdapterException) as excinfo:
        raise SlackEventAdapterException

    assert str(excinfo.value) == 'An error occurred in the SlackEventsApiAdapter library'
