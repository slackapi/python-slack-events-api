import json
from flask import Flask
import pytest
import sys
from slackeventsapi import SlackEventAdapter
from slackeventsapi.version import __version__


def test_existing_flask():
    valid_flask = Flask(__name__)
    valid_adapter = SlackEventAdapter("vFO9LARnLI7GflLR8tGqHgdy", "/slack/events", valid_flask)
    assert isinstance(valid_adapter, SlackEventAdapter)


def test_server_not_flask():
    with pytest.raises(TypeError) as e:
        invalid_flask = "I am not a Flask"
        SlackEventAdapter("vFO9LARnLI7GflLR8tGqHgdy", "/slack/events", invalid_flask)
    assert e.value.args[0] == 'Server must be an instance of Flask'


def test_event_endpoint_get(client):
    # GET on '/slack/events' should 404
    res = client.get('/slack/events')
    assert res.status_code == 404


def test_url_challenge(client):
    data = pytest.url_challenge_fixture
    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json')
    assert res.status_code == 200
    assert bytes.decode(res.data) == "valid_challenge_token"


def test_valid_event_request(client):
    data = pytest.reaction_event_fixture
    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json')
    assert res.status_code == 200


def test_version_header(client):
    # Verify [package metadata header is set
    python_version = "{:d}.{:d}".format(sys.version_info.major, sys.version_info.minor)
    pkg_info = "Python-{}/SlackEventAdapter-{}".format(python_version, __version__)

    data = pytest.reaction_event_fixture
    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json')

    assert res.status_code == 200
    assert res.headers["X-Slack-Adapter"] == pkg_info


def test_server_start(mocker):
    # Verify server started with correct params
    slack_events_adapter = SlackEventAdapter("token",)
    mocker.spy(slack_events_adapter, 'server')
    slack_events_adapter.start(port=3000)
    slack_events_adapter.server.run.assert_called_once_with(debug=False, host='127.0.0.1', port=3000)
