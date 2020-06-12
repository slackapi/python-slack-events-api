import json
import hashlib
import hmac
import pytest
from slackeventsapi import SlackEventAdapter


def create_signature(secret, timestamp, data):
    req = str.encode('v0:' + str(timestamp) + ':') + str.encode(data)
    request_signature= 'v0='+hmac.new(
        str.encode(secret),
        req, hashlib.sha256
    ).hexdigest()
    return request_signature


def load_event_fixture(event, as_string=True):
    filename = "tests/data/{}.json".format(event)
    with open(filename) as json_data:
        event_data = json.load(json_data)
        if not as_string:
            return event_data
        else:
            return json.dumps(event_data)


def event_with_bad_token():
    event_data = load_event_fixture('reaction_added', as_string=False)
    event_data['token'] = "bad_token"
    return json.dumps(event_data)


def pytest_configure():
    pytest.reaction_event_fixture = load_event_fixture('reaction_added')
    pytest.url_challenge_fixture = load_event_fixture('url_challenge')
    pytest.bad_token_fixture = event_with_bad_token()
    pytest.create_signature = create_signature

@pytest.fixture
def adapter():
    return SlackEventAdapter("SIGNING_SECRET")

@pytest.fixture
def app(adapter):
    app = adapter.server
    app.testing = True
    return app
