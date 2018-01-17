import json
from flask import Flask
import pytest
from slackeventsapi import SlackEventAdapter


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


def test_valid_event(client):
    data = pytest.reaction_event_fixture
    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json')
    assert res.status_code == 200
