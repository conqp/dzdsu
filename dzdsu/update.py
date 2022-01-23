"""Game and mod updates."""

from subprocess import CalledProcessError, CompletedProcess, run

from dzdsu.exceptions import FailedModUpdates
from dzdsu.mods import Mod
from dzdsu.server import Server


__all__ = ['ServerUpdater', 'steamcmd']


STEAMCMD = 'steamcmd'


class ServerUpdater:
    """Steam CMD commands."""

    def __init__(self, steam_user_name: str):
        self.steam_user_name = steam_user_name

    def update_server(self, server: Server) -> CompletedProcess:
        """Updates the server."""
        return steamcmd(
            '+force_install_dir', str(server.base_dir),
            '+login', self.steam_user_name,
            '+app_update', str(int(server.type)), 'validate'
        )

    def update_mod(self, server: Server, mod: Mod) -> CompletedProcess:
        """Updates a server's mod."""
        return steamcmd(
            '+force_install_dir', str(server.base_dir),
            '+login', self.steam_user_name,
            '+workshop_download_item', str(int(server.type)), str(mod.id),
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


def steamcmd(*commands: str) -> CompletedProcess:
    """Invokes steamcmd and exits."""

    return run([STEAMCMD, *commands, '+exit'], check=True)
