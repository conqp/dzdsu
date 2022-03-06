"""Extended RCon client."""

from time import sleep

from rcon import battleye


__all__ = ['Client']


class Client(battleye.Client):
    """RCon client with common methods."""

    def broadcast(self, message: str) -> str:
        """Broadcasts a message to all players."""
        return self.say(-1, message)

    def countdown(self, template: str, countdown: int) -> None:
        """Notify users about shutdown."""
        for passed in range(countdown):
            self.broadcast(template.format(countdown - passed))
            sleep(1)

            if self.passwd is not None:
                self.login(self.passwd)

    def kick(self, player: int | str, reason: str | None = None) -> str:
        """Kicks the respective player."""
        if reason is None:
            return self.run(f'kick {player}')

        return self.run(f'kick {player} {reason}')

    def say(self, player: int | str, message: str) -> str:
        """Say something to a player."""
        return self.run(f'say {player} {message}')

    def shutdown(self) -> str:
        """Shutdown the server."""
        return self.run('#shutdown')
