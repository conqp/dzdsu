"""Game and mod updates."""

from __future__ import annotations
from logging import getLogger
from subprocess import CompletedProcess, run

from dzdsu.constants import DAYZ_APP_ID, STEAMCMD
from dzdsu.server import Server


__all__ = ['Updater']


class Updater:
    """SteamCMD wrapper to update server and mods."""

    def __init__(self, server: Server, steam_user_name: str):
        """Sets server name and initial command."""
        self.server = server
        self.commands = [
            '+force_install_dir', str(server.base_dir),
            '+login', steam_user_name
        ]

    def __str__(self):
        """Returns the command as a string."""
        return ' '.join(self.command)

    def __call__(self) -> CompletedProcess:
        """Executes the steamcmd command."""
        getLogger('dzdsu').debug('Executing: %s', command := self.command)
        return run(command, check=True)

    @property
    def command(self) -> list[str]:
        """Returns the command."""
        return [STEAMCMD, *self.commands, '+quit']

    def update_server(self) -> Updater:
        """Updates the server."""
        self.commands += ['+app_update', str(self.server.app_id), 'validate']
        return self

    def update_mods(self) -> Updater:
        """Updates the server's mods."""
        for mod in self.server.enabled_mods:
            self.commands += [
                '+workshop_download_item', str(DAYZ_APP_ID), str(mod.id),
                'validate'
            ]

        return self
