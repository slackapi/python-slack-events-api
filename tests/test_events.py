import time
import pytest
from slackeventsapi import SlackEventAdapter

ADAPTER = SlackEventAdapter('SIGNING_SECRET')

def test_event_emission(client):
    # Events should trigger an event
    @ADAPTER.on('reaction_added')
    def event_handler(event):
        assert event["reaction"] == 'grinning'

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature(ADAPTER.signing_secret, timestamp, data)

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
