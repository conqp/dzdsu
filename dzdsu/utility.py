"""Server utility."""

from argparse import ArgumentParser, Namespace
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path

from dzdsu.constants import JSON_FILE
from dzdsu.keys import install_keys
from dzdsu.mods import print_mods
from dzdsu.server import load_servers
from dzdsu.update import Updater


__all__ = ['main']


LOGGER = getLogger('dzdsu')


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
        '-K', '--install-keys', action='store_true', help='install mod keys'
    )
    parser.add_argument(
        '-M', '--list-mods', action='store_true', help="list the server's mods"
    )
    parser.add_argument(
        '-U', '--update', metavar='steam_user', help='update server and mods'
    )
    parser.add_argument(
        '-s', '--update-server', action='store_true', help='update server'
    )
    parser.add_argument(
        '-m', '--update-mods', action='store_true',
        help="update the server's mods"
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging output'
    )
    return parser.parse_args()


def main() -> int:
    """Update mods."""

    args = get_args()
    basicConfig(level=INFO if args.verbose else WARNING)
    servers = load_servers(args.servers_file)

    try:
        server = servers[args.server]
    except KeyError:
        LOGGER.error('No such server: %s', args.server)
        return 2

    if args.install_keys:
        install_keys(args.directory)

    if args.update:
        updater = Updater(args.update)

        if args.update_server:
            updater.update_server(server)

        if args.update_mods:
            updater.update_mods(server)

    if args.list_mods:
        print_mods(server.mods, header='Mods')
        print_mods(server.server_mods, header='Server mods')

    return 0
