"""Game and mod updates."""

from subprocess import CalledProcessError, CompletedProcess, run

from dzdsu.constants import DAYZ_APP_ID, STEAMCMD
from dzdsu.exceptions import FailedModUpdates
from dzdsu.mods import Mod
from dzdsu.server import Server


__all__ = ['Updater', 'steamcmd']


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

    def update_mod(self, server: Server, mod: Mod) -> CompletedProcess:
        """Updates a server's mod."""
        return steamcmd(
            '+force_install_dir', str(server.base_dir),
            '+login', self.steam_user_name,
            '+workshop_download_item', str(DAYZ_APP_ID), str(mod.id),
            'validate'
        )

    def update_mods(self, server: Server) -> None:
        """Updates the server's mods."""
        failed_updates = set()

        for mod in server.mods:
            try:
                self.update_mod(server, mod)
            except CalledProcessError:
                failed_updates.add(mod)

        if failed_updates:
            raise FailedModUpdates(failed_updates)

    def update(self, server: Server) -> None:
        """Updates server and mods."""
        self.update_server(server)
        self.update_mods(server)


def steamcmd(*commands: str) -> CompletedProcess:
    """Invokes steamcmd and exits."""

    return run([STEAMCMD, *commands, '+exit'], check=True)
