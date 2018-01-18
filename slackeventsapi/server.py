from flask import Flask, request, make_response
from slackeventsapi.version import __version__
import json
import sys



class SlackServer(Flask):
    def __init__(self, verification_token, endpoint, emitter, server):
        self.verification_token = verification_token
        self.emitter = emitter
        self.endpoint = endpoint

        # If a server is passed in, bind the event handler routes to it,
        # otherwise create a new Flask instance.
        if server:
            if isinstance(server, Flask):
                self.bind_route(server)
            else:
                raise TypeError("Server must be an instance of Flask")
        else:
            Flask.__init__(self, __name__)
            self.bind_route(self)

    def bind_route(self, server):
        @server.route(self.endpoint, methods=['GET', 'POST'])
        def event():
            # If a GET request is made, return 404.
            if request.method == 'GET':
                return make_response("These are not the slackbots you're looking for.", 404)

            # Parse the request payload into JSON
            event_data = json.loads(request.data.decode('utf-8'))

            # Echo the URL verification challenge code
            if "challenge" in event_data:
                return make_response(
                    event_data.get("challenge"), 200, {"content_type": "application/json"}
                )

            # Verify the request token
            request_token = event_data.get("token")
            if self.verification_token != request_token:
                self.emitter.emit('error', 'invalid verification token')
                return make_response("Request contains invalid Slack verification token", 403)

            # Parse the Event payload and emit the event to the event listener
            if "event" in event_data:
                event_type = event_data["event"]["type"]
                self.emitter.emit(event_type, event_data)
                response = make_response("", 200)
                python_version = "{:d}.{:d}".format(sys.version_info.major, sys.version_info.minor)
                pkg_info = "Python-{}/SlackEventAdapter-{}".format(python_version, __version__)
                response.headers['X-Slack-Adapter'] = pkg_info
                return response
