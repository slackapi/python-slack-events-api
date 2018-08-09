import hmac
import hashlib
import time
import pytest
from slackeventsapi import SlackEventAdapter

ADAPTER = SlackEventAdapter('SIGNING_SECRET')

def create_signature(secret, timestamp, data):
    req = str.encode('v0:' + str(timestamp) + ':') + data
    request_signature= 'v0='+hmac.new(
        str.encode(secret),
        req, hashlib.sha256
    ).hexdigest()
    return request_signature


def test_event_emission(client):
    # Events should trigger an event
    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature =create_signature(ADAPTER.signing_secret, timestamp, data)

    @ADAPTER.on('reaction_added')
    def event_handler(event):
        assert event["reaction"] == 'grinning'

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
