"""Handle logging."""

from ..handler import Handler


class LoggingHandler(Handler):
    """Logging handler."""

    def on_message(self, packet):
        """Handle message events."""
        self.logger.debug(packet)
        self.logger.info(
            packet["user"],
            ''.join(chunk["text"] for chunk in packet if
                    chunk["type"] == chunk["text"])
        )

    def on_follow(self, packet):
        """Handle follow events."""
        self.logger.debug(packet)
        self.logger.info("- %s followed", packet["user"])

    def on_subscribe(self, packet):
        """Handle subscription events."""
        self.logger.debug(packet)
        self.logger.info("- %s subscribed", packet["user"])

    def on_resubscribe(self, packet):
        """Handle resubscription events."""
        self.logger.debug(packet)
        self.logger.info("- %s resbscribed", packet["user"])

    def on_host(self, packet):
        """Handle host events."""
        self.logger.debug(packet)
        self.logger.info("- %s hosted", packet["user"])

    def on_join(self, packet):
        """Handle user join events."""
        self.logger.debug(packet)
        self.logger.info("- %s joined", packet["user"])
