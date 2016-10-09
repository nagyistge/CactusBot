"""Handle data from Beam."""

import logging

import asyncio

from .api import BeamAPI
from .chat import BeamChat
from .constellation import BeamConstellation
from .parser import BeamParser
from ...packets import MessagePacket, BanPacket


class BeamHandler:
    """Handle data from Beam services."""

    def __init__(self, channel, handlers):

        self.logger = logging.getLogger(__name__)

        self.api = BeamAPI()
        self.parser = BeamParser()
        self.handlers = handlers  # HACK, potentially

        self._channel = channel
        self.channel = ""

        self.chat = None
        self.constellation = None

        self.chat_events = {
            "ChatMessage": "message"
        }

        self.constellation_events = {
            "channel:followed": "follow",
            "channel:subscribed": "subscribe",
            "channel:hosted": "host"
        }

    async def run(self, *auth):
        """Connect to Beam chat and handle incoming packets."""
        channel = await self.api.get_channel(self._channel)
        self.channel = str(channel["id"])
        self.api.channel = self.channel  # HACK

        user = await self.api.login(*auth)
        chat = await self.api.get_chat(channel["id"])

        self.chat = BeamChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(user["id"], chat["authkey"])
        asyncio.ensure_future(self.chat.read(self.handle_chat))

        self.constellation = BeamConstellation(channel["id"], user["id"])
        await self.constellation.connect()
        asyncio.ensure_future(
            self.constellation.read(self.handle_constellation))

        await self.send(MessagePacket(
            ("text", "Cactusbot activated. "),
            ("emote", "cactus", ":cactus")   
        ))

    async def handle_chat(self, packet):
        """Handle chat packets."""

        data = packet.get("data")
        if data is None:
            return

        event = packet.get("event")

        if event in self.chat_events:
            event = self.chat_events[event]

            # HACK
            if getattr(self.parser, "parse_" + event):
                data = getattr(self.parser, "parse_" + event)(data)

            for response in self.handlers.handle(event, data):
                if isinstance(response, MessagePacket):
                    text = self.parser.synthesize(response)
                elif isinstance(response, BanPacket):
                    await self.timeout(packet.user, response.time)
                await self.send(text)

    async def handle_constellation(self, packet):
        """Handle constellation packets."""

        if "data" not in packet:
            return
        data = packet["data"]["payload"]

        scope, _, event = packet["data"]["channel"].split(":")
        event = scope + ':' + event

        if event in self.constellation_events:
            event = self.constellation_events[event]

            # HACK
            if getattr(self.parser, "parse_" + event):
                data = getattr(self.parser, "parse_" + event)(data)

            for response in self.handlers.handle(event, data):
                await self.send(response.text)  # HACK

    async def send(self, *args, **kwargs):
        """Send a packet to Beam."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)
