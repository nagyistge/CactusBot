"""Interact with Mixer Constellation."""

import re
import json

from .. import WebSocket


class MixerConstellation(WebSocket):
    """Interact with Mixer Constellation."""

    URL = "wss://constellation.mixer.com"

    RESPONSE_EXPR = re.compile(r'^(\d+)(.+)?$')
    INTERFACE_EXPR = re.compile(r'^([a-z]+):\d+:([a-z]+)')

    def __init__(self, channel, user):
        super().__init__(self.URL)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

    async def initialize(self, *interfaces):
        """Subscribe to Constellation interfaces."""

        if not interfaces:
            interfaces = (
                "channel:{channel}:update",
                "channel:{channel}:status",
                "channel:{channel}:followed",
                "channel:{channel}:subscribed",
                "channel:{channel}:resubscribed",
                "channel:{channel}:hosted",
                "user:{user}:followed",
                "user:{user}:subscribed",
                "user:{user}:achievement"
            )

        interfaces = [
            interface.format(channel=self.channel, user=self.user)
            for interface in interfaces
        ]

        packet = {
            "type": "method",
            "method": "livesubscribe",
            "params": {
                "events": interfaces
            },
            "id": 1
        }

        await self._send(json.dumps(packet))
        await self.receive()

        self.logger.info(
            "Successfully subscribed to Constellation interfaces.")

    parse = WebSocket._parse_json()