from flask import Flask, request, make_response
import json


class SlackServer(Flask):
    def __init__(self, verification_token, endpoint, emitter):
        Flask.__init__(self, __name__)
        self.verification_token = verification_token

        @self.route(endpoint, methods=['GET', 'POST'])
        def event():
            # If a GET request is made, return 404.
            if request.method == 'GET':
                return make_response("These are not the slackbots you're looking for.", 404)

            # Parse the request payload into JSON
            event_data = json.loads(request.data)

            # Echo the URL verification challenge code
            if "challenge" in event_data:
                return make_response(
                    event_data.get("challenge"), 200, {"content_type": "application/json"}
                )

            # Parse the Event payload and emit the event to the event listener
            if "event" in event_data:
                # Verify the request token
                request_token = event_data.get("token")
                if self.verification_token != request_token:
                    emitter.emit('error', 'invalid verification token')
                    message = "Request contains invalid Slack verification token: %s\n" \
                              "Slack adapter has: %s" % (request_token, self.verification_token)
                    return make_response(message, 403)

                event_type = event_data["event"]["type"]
                emitter.emit(event_type, event_data)
                return make_response("", 200)
