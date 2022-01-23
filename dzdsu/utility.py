"""Server utility."""

from argparse import ArgumentParser, Namespace
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path

from dzdsu.constants import KEYS_GLOB


LOGGER = getLogger('dzdsu')


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        'directory', type=Path, default=Path.cwd(),
        help='target directory to unpack into'
    )
    parser.add_argument(
        '-K', action='store_true', help='install mod keys'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging output'
    )
    return parser.parse_args()


def install_keys(base_dir: Path) -> None:
    """Installs the mod keys."""

    for key in base_dir.glob(KEYS_GLOB):
        LOGGER.info('Installing key: %s', key.name)

        with base_dir.joinpath('keys').joinpath(key.name).open('wb') as dst:
            with key.open('rb') as src:
                dst.write(src.read())


def main() -> int:
    """Update mods."""

    args = get_args()
    basicConfig(level=INFO if args.verbose else WARNING)

    if args.install_keys:
        install_keys(args.directory)
    else:
        LOGGER.warning('No action selected.')
        return 2

    return 0
