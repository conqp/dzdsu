"""Game and mod updates."""

from itertools import chain
from logging import getLogger
from subprocess import CompletedProcess, run

from dzdsu.constants import DAYZ_APP_ID, STEAMCMD
from dzdsu.mods import Mod
from dzdsu.server import Server


__all__ = ['Updater', 'steamcmd']


LOGGER = getLogger('Updater')


class Updater:
    """SteamCMD wrapper to update server and mods."""

    def __init__(self, steam_user_name: str):
        self.steam_user_name = steam_user_name

    def update_server(self, server: Server) -> CompletedProcess:
        """Updates the server."""
        return steamcmd(
            '+force_install_dir', str(server.base_dir),
            '+login', self.steam_user_name,
            '+app_update', str(server.app_id), 'validate'
        )

    def update_mods(self, server: Server) -> CompletedProcess:
        """Updates the server's mods."""
        return steamcmd(
            '+force_install_dir', str(server.base_dir),
            '+login', self.steam_user_name,
            *chain(*(update_mod_command(mod) for mod in server.mods))
        )

    def update(self, server: Server) -> None:
        """Updates server and mods."""
        self.update_server(server)
        self.update_mods(server)


def steamcmd(*commands: str) -> CompletedProcess:
    """Invokes steamcmd and exits."""

    return run([STEAMCMD, *commands, '+quit'], check=True)


def update_mod_command(mod: Mod) -> list[str]:
    """Returns a steamcmd command to update the given mod."""

    return [
        '+workshop_download_item', str(DAYZ_APP_ID), str(mod.id), 'validate'
    ]
