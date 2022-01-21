"""Pack mods from a local installation for a dedicated server."""

from argparse import ArgumentParser, Namespace
from logging import INFO, WARNING, basicConfig, getLogger
from os import environ, name
from pathlib import Path
from sys import exit, stderr
from tarfile import open
from typing import Iterator


FILENAME = 'dayz-mods.tar.gz'
LOGGER = getLogger(__file__)
MODS_DIR = Path('steamapps/common/DayZ/!Workshop')

if name == 'nt':
    STEAM_DIR = Path(environ.get("PROGRAMFILES(X86)")) / 'Steam'
elif name == 'posix':
    STEAM_DIR = Path.home() / '.steam'
else:
    LOGGER.error('Unsupported operating system: %s.', name)
    exit(1)


def get_args(description: str = __doc__) -> Namespace:
    """Returns the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-s', '--steam-dir', type=Path, default=STEAM_DIR, metavar='dir',
        help='Steam base directory'
    )
    parser.add_argument(
        '-m', '--mods-dir', type=Path, metavar='dir', help='mods directory'
    )
    parser.add_argument(
        '-f', '--file', type=Path, default=Path.cwd() / FILENAME,
        metavar='filename', help='output file name'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging output'
    )
    return parser.parse_args()


def get_mods(mods_dir: Path) -> Iterator[Path]:
    """Yields mod directories in the mods dir."""

    return filter(lambda mod: mod.name.startswith('@'), mods_dir.iterdir())


def pack_directory(mods_dir: Path, tar_file: Path) -> None:
    """Packs the mods in the given mod folder into a tar file."""

    with tar_file.open('wb') as file:
        LOGGER.info('Packing mods from %s into: %s', mods_dir, tar_file)

        with open(fileobj=file, mode='w:gz') as tar:
            for mod in get_mods(mods_dir):
                LOGGER.info('Adding mod: %s', mod.name)
                tar.add(mod, arcname=mod.name.replace(' ', '_'))


def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(level=INFO if args.verbose else WARNING)
    mods_dir = args.mods_dir or (args.steam_dir / MODS_DIR)
    pack_directory(mods_dir, args.file)


if __name__ == '__main__':
    main()
