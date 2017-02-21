import pytest
from slackeventsapi import SlackEventAdapter

ADAPTER = SlackEventAdapter('vFO9LARnLI7GflLR8tGqHgdy')


def test_event_emission(client):
    # Events should trigger an event
    data = pytest.reaction_event_fixture

    @ADAPTER.on('reaction_added')
    def event_handler(event):
        assert event["reaction"] == 'grinning'

    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json'
    )

    assert res.status_code == 200
