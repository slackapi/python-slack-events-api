import time
import pytest

from slackeventsapi.server import SlackEventAdapterException

def test_event_emission(adapter):
    test_event_emission.event_handled = False

    # Events should trigger an event
    @adapter.on('reaction_added')
    def event_handler(event_data):
        test_event_emission.event_handled = True

        event = event_data['event']
        assert event["reaction"] == 'grinning'

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature(adapter.signing_secret, timestamp, data)

    with adapter.server.test_client() as client:
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

    assert test_event_emission.event_handled

def test_error_timestamp(adapter):
    test_error_timestamp.event_handled = False

    # Error should trigger an event
    @adapter.on('error')
    def event_handler(exception):
        test_error_timestamp.event_handled = True
        assert isinstance(exception, SlackEventAdapterException)
        assert str(exception) == 'Invalid request timestamp'

    data = pytest.reaction_event_fixture

    # Set timestamp to Thu Jan 01 00:00:00 1970 UTC (Epoch 0)
    timestamp = 0

    signature = pytest.create_signature(adapter.signing_secret, timestamp, data)

    with adapter.server.test_client() as client:
        res = client.post(
            '/slack/events',
            data=data,
            content_type='application/json',
            headers={
                'X-Slack-Request-Timestamp': timestamp,
                'X-Slack-Signature': signature
            }
        )
        assert res.status_code == 403

    assert test_error_timestamp.event_handled

def test_error_signature(adapter):
    test_error_signature.event_handled = False

    # Error should trigger an event
    @adapter.on('error')
    def event_handler(exception):
        test_error_signature.event_handled = True
        assert isinstance(exception, SlackEventAdapterException)
        assert str(exception) == 'Invalid request signature'

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature('INVALID SIGNATURE', timestamp, data)

    with adapter.server.test_client() as client:
        res = client.post(
            '/slack/events',
            data=data,
            content_type='application/json',
            headers={
                'X-Slack-Request-Timestamp': timestamp,
                'X-Slack-Signature': signature
            }
        )
        assert res.status_code == 403

    assert test_error_signature.event_handled
