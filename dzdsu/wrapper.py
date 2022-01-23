"""DayZ server wrapper."""

from argparse import ArgumentParser, Namespace
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path
from subprocess import run

from dzdsu.constants import JSON_FILE
from dzdsu.server import load_servers


LOGGER = getLogger('dzds')


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-f', '--servers-file', type=Path, default=JSON_FILE, metavar='file',
        help='servers JSON file path'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging'
    )
    return parser.parse_args()


def main() -> int:
    """Starts the DayZ server."""

    args = get_args()
    basicConfig(level=INFO if args.verbose else WARNING)
    servers = load_servers(args.servers_file)

    try:
        server = servers[args.server]
    except KeyError:
        LOGGER.error('No such server: %s', args.server)
        return 2

    return run(server.command, check=False).returncode
