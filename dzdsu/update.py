"""Game and mod updates."""

from subprocess import CompletedProcess, run

from dzdsu.constants import DAYZ_APP_ID, STEAMCMD
from dzdsu.server import Server


__all__ = ['Updater']


class Updater:
    """SteamCMD wrapper to update server and mods."""

    def __init__(self, server: Server, steam_user_name: str):
        self.server = server
        self.commands = [
            '+force_install_dir', str(server.base_dir),
            '+login', steam_user_name
        ]

    def update_server(self) -> None:
        """Updates the server."""
        self.commands += ['+app_update', str(self.server.app_id), 'validate']

    def update_mods(self) -> None:
        """Updates the server's mods."""
        for mod in self.server.used_mods:
            self.commands += [
                '+workshop_download_item', str(DAYZ_APP_ID), str(mod.id),
                'validate'
            ]

    def execute(self) -> CompletedProcess:
        """Executes the steamcmd command."""
        return run([STEAMCMD, *self.commands, '+quit'], check=True)
