"""Keys handling."""

from logging import getLogger
from pathlib import Path

from dzdsu.constants import KEYS_GLOB, MODS_BASE_DIR


__all__ = ['install_keys']


LOGGER = getLogger('keys-installer')


def install_keys(base_dir: Path, *, overwrite: bool = False) -> None:
    """Installs the mod keys."""

    for src_file in (base_dir / MODS_BASE_DIR).glob(KEYS_GLOB):
        LOGGER.info('Installing key: %s', (name := src_file.name))

        if (dst_file := (base_dir / 'keys' / src_file.name)).exists():
            LOGGER.warning('Key "%s" already installed.', name)

            if not overwrite:
                continue

        with dst_file.open('wb') as dst, src_file.open('rb') as src:
            dst.write(src.read())
