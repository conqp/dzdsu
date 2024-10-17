"""Extended RCon client."""
from contextlib import suppress
from threading import Thread
from time import sleep

from rcon import battleye

__all__ = ["Client"]

from rcon.battleye import ServerMessage


class Client(battleye.Client):
    """RCon client with common methods."""

    running: bool

    def broadcast(self, message: str) -> str:
        """Broadcasts a message to all players."""
        return self.say(-1, message)

    def countdown(
            self, template: str, countdown: int, *, every: int = 10,
            always_below: int = 30
    ) -> None:
        """Notify users about shutdown."""
        first = True
        self.running = True
        thread = Thread(target=self._handle_server_messages, daemon=True)
        thread.start()

        for passed in range(countdown):
            remaining = countdown - passed

            if first or remaining % every == 0 or remaining < always_below:
                first = False
                self.broadcast(template.format(remaining))

            sleep(1)

        self.running = False

    def kick(self, player: int | str, reason: str | None = None) -> str:
        """Kicks the respective player."""
        if reason is None:
            return self.run(f"kick {player}")

        return self.run(f"kick {player} {reason}")

    def say(self, player: int | str, message: str) -> str:
        """Say something to a player."""
        return self.run(f"say {player} {message}")

    def shutdown(self) -> str:
        """Shutdown the server."""
        return self.run("#shutdown")

    def _handle_server_messages(self):
        """Handle server messages."""
        while self.running:
            with suppress(TimeoutError):
                if isinstance(response := self.receive(), ServerMessage):
                    self.handle_server_message(response)
