#! /usr/bin/env python3
"""Install packed mods."""

from argparse import ArgumentParser, Namespace
from functools import partial
from hashlib import sha1
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path
from tarfile import open
from typing import Optional


FILENAME = 'dayz-mods.tar.gz'
HASH_FILE = '.mods.sha1.txt'
LOGGER = getLogger(__file__)


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        'file', type=Path, default=Path.cwd() / FILENAME,
        help='tar file of the mods to install'
    )
    parser.add_argument(
        'directory', type=Path, default=Path.cwd(),
        help='target directory to unpack into'
    )
    parser.add_argument(
        '--hash-cache', type=Path, default=Path.cwd() / HASH_FILE,
        help='hash cache file'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging output'
    )
    return parser.parse_args()


def get_last_hash(filename: Path) -> Optional[str]:
    """Returns the hash of the last mod pack."""

    try:
        with filename.open('r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def store_hash(filename: Path, sha1sum: str) -> None:
    """Stores the hash."""

    with filename.open('w') as file:
        file.write(sha1sum)


def get_sha1_hash(filename: Path, *, chunk_size: int = 4096) -> str:
    """Returns the SHA-1 hash of the given file."""

    sha1sum = sha1()

    with filename.open('rb') as file:
        for chunk in iter(partial(file.read, chunk_size), b''):
            sha1sum.update(chunk)

    return sha1sum.hexdigest()


def extract_mods(tar_file: Path, target_dir: Path) -> None:
    """Extracts the mods."""

    with open(tar_file, mode='r:*') as tar:
        LOGGER.info('Extracting mods...')
        tar.extractall(path=target_dir)


def main() -> None:
    """Update mods."""

    args = get_args()
    basicConfig(level=INFO if args.verbose else WARNING)
    last_hash = get_last_hash(args.hash_cache)
    LOGGER.info('Last hash: %s', last_hash)
    sha1sum = get_sha1_hash(args.file)
    LOGGER.info('Current hash: %s', sha1sum)

    if last_hash == sha1sum:
        LOGGER.warning('No update necessary.')
        return

    extract_mods(args.file, args.directory)
    store_hash(args.hash_cache, sha1sum)


if __name__ == '__main__':
    main()
