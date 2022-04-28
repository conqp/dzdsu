"""Updating of the server."""

from argparse import Namespace
from os import name
from time import sleep

from dzdsu.constants import MESSAGE_TEMPLATE_UPDATE, UNSUPPORTED_OS
from dzdsu.hash import hash_changed
from dzdsu.server import Server
from dzdsu.update import Updater
from dzdsu.utility.logger import LOGGER
from dzdsu.utility.shutdown import shutdown


__all__ = ['update']


def update(server: Server, args: Namespace) -> None:
    """Updates the server."""

    if name == 'nt':
        return _update_nt(server, args)

    if name == 'posix':
        return _update_posix(server, args)

    raise UNSUPPORTED_OS


def _update_nt(server: Server, args: Namespace) -> None:
    """Update NT systems."""

    # Windows systems cannot override files that are in use by a process.
    # So we need to shut the server down *before* the update.
    if not _nt_pre_update_shutdown(server, args):
        return

    LOGGER.info('Waiting for server to shut down.')

    with server.update_lockfile:
        _await_shutdown(server)
        _update(server, args)


def _update_posix(server: Server, args: Namespace) -> None:
    """Update POSIX systems."""

    with server.update_lockfile:
        _update(server, args)


def _await_shutdown(server: Server) -> None:
    """Wait for the server to shut down."""

    while server.is_running:
        print('.', end='', flush=True)
        sleep(1)

    print()


def _nt_pre_update_shutdown(server: Server, args: Namespace) -> bool:
    """Conditionally shutdown server before update on NT platforms."""

    if not (args.force or _nt_needs_update(server, args)):
        LOGGER.info('No update required.')
        return False

    LOGGER.info('Updates detected. Notifying users.')

    if not shutdown(
            server,
            args.message or MESSAGE_TEMPLATE_UPDATE,
            args.countdown
    ):
        LOGGER.error('Could not shutdown server prior to update.')
        return False

    return True


def _nt_needs_update(server: Server, args: Namespace) -> bool:
    """Returns True iff there is an update available on an NT platform."""

    # Since we cannot update the server on NT while it is running,
    # we need to install a copy of the server and all its mods.
    # Then we can compare the copy's hashes to the running server's hashes
    # to check whether an update is available.
    server.copy_dir.mkdir(exist_ok=True)
    _update(copy := server.chdir(server.copy_dir), args)
    return hash_changed(server.hashes, copy.hashes)


def _update(server: Server, args: Namespace) -> None:
    """Perform server and mod updates."""

    updater = Updater(server, args.update)

    if args.update_server:
        updater.update_server()

    if args.update_mods:
        updater.update_mods()

    updater()
    print()
