from pyee import EventEmitter
from .server import SlackServer


class SlackEventAdapter(EventEmitter):
    # Initialize the Slack event server
    # If no endpoint is provided, default to listening on '/slack/events'
    # **kwargs:
    #   If no health_endpoint is provided, default defined as '/health' in
    #   server.py
    #
    #   If no health_callback is provided, default is 200 healthy in
    #   server.py. A provided health_callback function must require no
    #   arguments and return a Flask-compatible response.
    def __init__(self, verification_token, endpoint="/slack/events", **kwargs):
        EventEmitter.__init__(self)
        self.verification_token = verification_token
        self.server = SlackServer(verification_token, endpoint, self, **kwargs)

    def start(self, host='127.0.0.1', port=None, debug=False, **kwargs):
        self.server.run(host=host, port=port, debug=debug, **kwargs)
