"""Updating of the server."""

from argparse import Namespace
from os import name

from dzdsu.hash import hash_changed
from dzdsu.server import Server
from dzdsu.update import Updater
from dzdsu.utility.logger import LOGGER
from dzdsu.utility.shutdown import shutdown


__all__ = ['update']


def update(server: Server, args: Namespace) -> None:
    """Updates the server."""

    # Windows systems cannot override files that are in use by a process.
    # So we need to shut the server down *before* the update.
    if name == 'nt' and not _nt_pre_update_shutdown(server, args):
        return

    _update(server, args)


def _nt_pre_update_shutdown(server: Server, args: Namespace) -> bool:
    """Conditionally shutdown server before update on NT platforms."""

    if not _nt_needs_update(server, args):
        LOGGER.info('No update required.')
        return False

    LOGGER.info('Updates detected. Notifying users.')

    if not shutdown(server, args):
        LOGGER.warning('Could not shutdown server prior to update.')
        return False

    return True


def _nt_needs_update(server: Server, args: Namespace) -> bool:
    """Returns True iff there is an update available on an NT platform."""

    # Since we cannot update the server on NT while it is running,
    # we need to install a copy of the server.
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

    with server.update_lockfile:
        updater()
