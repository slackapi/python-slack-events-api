import json
import pytest


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
    assert res.data == "valid_challenge_token"


def test_valid_event(client):
    data = pytest.reaction_event_fixture
    res = client.post(
        '/slack/events',
        data=data,
        content_type='application/json')
    assert res.status_code == 200

@pytest.mark.health_ok
def test_default_health_endpoint(client):
    res = client.get('/health')
    assert res.status_code == 200

@pytest.mark.health_ok
@pytest.mark.health_custom
def test_custom_ok_health_endpoint(client):
    res = client.get('/health_custom')
    assert res.status_code == 200

@pytest.mark.health_unavailable
@pytest.mark.health_custom
def test_custom_unavailable_health_endpoint(client):
    res = client.get('/health_custom')
    assert res.status_code == 503
