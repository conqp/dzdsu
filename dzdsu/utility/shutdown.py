"""Server shutdown."""

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['shutdown']


def shutdown(server: Server, message: str, countdown: int) -> bool:
    """Shut down the server iff it needs a restart."""

    if not server.countdown(message, countdown=countdown):
        LOGGER.error('Could not notify users about shutdown.')
        return False

    LOGGER.info(f'Kicking remaining users.')
    server.kick_all('Server restart.')
    LOGGER.info(f'Stopping server.')
    server.shutdown()
    return True
