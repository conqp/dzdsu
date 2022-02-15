"""Game and mod updates."""

from __future__ import annotations
from subprocess import CompletedProcess, run

from dzdsu.constants import DAYZ_APP_ID, STEAMCMD, STEAMCMD_WINE, WINE
from dzdsu.server import Server


__all__ = ['Updater']


class Updater:
    """SteamCMD wrapper to update server and mods."""

    def __init__(self, server: Server, steam_user_name: str):
        """Sets server name and initial command."""
        self.server = server
        self.commands = [
            '+force_install_dir', server.install_dir,
            '+login', steam_user_name
        ]

    def __str__(self):
        """Returns the command as a string."""
        return ' '.join(self.command)

    def __call__(self) -> CompletedProcess:
        """Executes the steamcmd command."""
        return run(self.command, check=True)

    @property
    def steamcmd(self) -> list[str]:
        """Returns the steamcmd command and args list."""
        if self.server.wine:
            return [WINE, str(self.server.base_dir / STEAMCMD_WINE)]

        return [STEAMCMD]

    @property
    def command(self) -> list[str]:
        """Returns the command."""
        return [*self.steamcmd, *self.commands, '+quit']

    def update_server(self) -> Updater:
        """Updates the server."""
        self.commands += ['+app_update', str(self.server.app_id), 'validate']
        return self

    def update_mods(self) -> Updater:
        """Updates the server's mods."""
        for mod in self.server.used_mods:
            self.commands += [
                '+workshop_download_item', str(DAYZ_APP_ID), str(mod.id),
                'validate'
            ]

        return self
