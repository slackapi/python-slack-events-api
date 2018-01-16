from pyee import EventEmitter
from .server import SlackServer


class SlackEventAdapter(EventEmitter):
    # Initialize the Slack event server
    # If no endpoint is provided, default to listening on '/slack/events'
    def __init__(self, verification_token, endpoint="/slack/events", server=None):
        EventEmitter.__init__(self)
        self.verification_token = verification_token
        self.server = SlackServer(verification_token, endpoint, self, server)

    def start(self, host='127.0.0.1', port=None, debug=False, **kwargs):
        """
        Start the built in webserver, bound to the host and port you'd like.
        Default host is `127.0.0.1` and port 8080.

        :param host: The host you want to bind the build in webserver to
        :param port: The port number you want the webserver to run on
        :param debug: Set to `True` to enable debug level logging
        :param kwargs: Additional arguments you'd like to pass to Flask
        """
        self.server.run(host=host, port=port, debug=debug, **kwargs)
