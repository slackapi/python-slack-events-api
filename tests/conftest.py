import pytest
import json
from flask import make_response
from slackeventsapi import SlackEventAdapter


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


def pytest_namespace():
    return {
        'reaction_event_fixture': load_event_fixture('reaction_added'),
        'url_challenge_fixture': load_event_fixture('url_challenge'),
        'bad_token_fixture': event_with_bad_token()
    }


@pytest.fixture()
def app(request):
    if request.node.get_marker('health_custom') is not None and request.node.get_marker('health_ok') is not None:
        def health():
            return make_response('healthy', 200)
        adapter = SlackEventAdapter("vFO9LARnLI7GflLR8tGqHgdy", health_endpoint='/health_custom', health_callback=health)
        app = adapter.server
        return app
    elif request.node.get_marker('health_custom') is not None and request.node.get_marker('health_unavailable') is not None:
        def health():
            return make_response('not ready', 503)
        adapter = SlackEventAdapter("vFO9LARnLI7GflLR8tGqHgdy", health_endpoint='/health_custom', health_callback=health)
        app = adapter.server
        return app

    adapter = SlackEventAdapter("vFO9LARnLI7GflLR8tGqHgdy")
    app = adapter.server
    return app
