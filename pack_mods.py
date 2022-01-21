"""Pack mods from a local installation for a dedicated server."""

from argparse import ArgumentParser, Namespace
from os import environ, name
from pathlib import Path
from sys import exit, stderr
from tarfile import TarFile, open
from typing import Iterator


if name != 'nt':
    print('This script runs on Windows only.', file=stderr)
    exit(1)


FILENAME = 'dayz-mods.tar.gz'
MODS_DIR = Path('steamapps/common/DayZ/!Workshop')
STEAM_DIR = Path(environ.get("PROGRAMFILES(X86)")) / 'Steam'


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
    return parser.parse_args()


def get_mods(mods_dir: Path) -> Iterator[Path]:
    """Yields mod directories in the mods dir."""

    return filter(lambda mod: mod.name.startswith('@'), mods_dir.iterdir())


def get_archive_name(mod_name: str) -> str:
    """Returns the archive name of the mod."""

    return mod_name.replace(' ', '_')


def add_mods(tar: TarFile, mods_dir: Path) -> None:
    """Packs mods into the tar file."""

    for mod in get_mods(mods_dir):
        tar.add(mod, arcname=get_archive_name(mod.name))


def pack_directory(mods_dir: Path, tar_file: Path) -> None:
    """Packs the mods in the given mod folder into a tar file."""

    with tar_file.open('wb') as file:
        with open(fileobj=file, mode='w:gz') as tar:
            add_mods(tar, mods_dir)


def main() -> None:
    """Runs the script."""

    args = get_args()
    mods_dir = args.mods_dir or (args.steam_dir / MODS_DIR)
    pack_directory(mods_dir, args.file)


if __name__ == '__main__':
    main()
