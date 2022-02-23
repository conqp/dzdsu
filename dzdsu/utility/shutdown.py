"""Server shutdown."""

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['shutdown']


def shutdown(server: Server, message: str, countdown: int) -> bool:
    """Shut down the server iff it needs a restart."""

    if not server.is_running:
        return True

    try:
        server.countdown(message, countdown=countdown)
    except (ConnectionRefusedError, TimeoutError, ConnectionResetError):
        LOGGER.error('Could not notify users about shutdown.')
        return False

    LOGGER.info('Kicking remaining players.')

    try:
        server.kick_all('Server restart.')
    except (ConnectionRefusedError, TimeoutError, ConnectionResetError):
        LOGGER.warning('Could not kick all remaining players.')

    LOGGER.info('Stopping server.')

    try:
        server.shutdown()
    except (ConnectionRefusedError, TimeoutError, ConnectionResetError):
        return False

    return True
