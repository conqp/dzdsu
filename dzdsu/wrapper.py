"""Server wrapper."""

from argparse import ArgumentParser, Namespace
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path
from subprocess import Popen

from dzdsu.constants import JSON_FILE
from dzdsu.server import load_servers


__all__ = ['main']


LOGGER = getLogger('dzdsw')


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        'server', default=Path.cwd().name,
        help='the name of the server to start'
    )
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

    Popen(server.command, cwd=server.base_dir)
    return 0
