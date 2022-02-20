"""Mod-related actions."""

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['clean_mods', 'fix_mod_paths', 'install_keys']


def clean_mods(server: Server) -> None:
    """Remove unused mods."""

    for installed_mod in server.unused_mods:
        LOGGER.info('Removing unused mod: %s', installed_mod.mod)
        installed_mod.remove()


def fix_mod_paths(server: Server) -> None:
    """Fix paths of the server mods."""

    for installed_mod in server.installed_mods:
        LOGGER.info('Fixing paths of: %s', installed_mod.mod)
        installed_mod.fix_paths()


def install_keys(server: Server) -> None:
    """Installs the keys for all mods of the server."""

    for installed_mod in server.installed_mods:
        for key in installed_mod.bikeys:
            if (installed := server.base_dir / 'keys' / key.name).exists():
                LOGGER.info('Key "%s" already installed.', key.name)
                continue

            with key.open('rb') as src, installed.open('wb') as dst:
                dst.write(src.read())
