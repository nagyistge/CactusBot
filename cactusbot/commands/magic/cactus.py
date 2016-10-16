"""Cactus Command."""


from . import Command
from ...packets import MessagePacket

class Cactus(Command):
    """Ouch! That's pokey!"""

    COMMAND = "cactus"

    @Command.subcommand()
    async def cactus(self):
        return MessagePacket(
            ("text", "Ohai! I'm CactusBot! "),
            ("emoji", ":cactus:", ":cactus:")
        )

    @Command.subcommand
    async def docs(self):
        return MessagePacket(
            ("text", "Check out my documentation at "),
            ("link", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
            ("text", ".")
        )

    @Command.subcommand
    async def help(self):
        return "Try our docs (!cactus docs). If that doesn't help, tweet at us (!cactus twitter)!"
    
    @Command.subcommand()
    async def twitter(self):
        return MessagePacket(
            ("text", "You can follow the team behind CactusBot at: "),
            ("link", "https://twitter.com/CactusDevTeam", "twitter.com/CactusDevTeam")
        )

    DEFAULT = cactus