"""Server utility."""

from argparse import ArgumentParser, Namespace
from itertools import chain
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path

from dzdsu.constants import JSON_FILE
from dzdsu.mods import ModMetadata, print_mods
from dzdsu.server import Server, load_servers
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
        '-F', '--fix-paths', action='store_true', help='fix mod file paths'
    )
    parser.add_argument(
        '-I', '--installed-mods', action='store_true',
        help='list installed mods'
    )
    parser.add_argument(
        '-K', '--install-keys', action='store_true', help='install mod keys'
    )
    parser.add_argument(
        '-M', '--list-mods', action='store_true', help="list the server's mods"
    )
    parser.add_argument(
        '-U', '--update', metavar='steam_user',
        help='provide steam user to update server and/or mods'
    )
    parser.add_argument(
        '-s', '--update-server', action='store_true', help='update server'
    )
    parser.add_argument(
        '-m', '--update-mods', action='store_true',
        help="update the server's mods"
    )
    parser.add_argument(
        '--overwrite', action='store_true', help="overwrite existing key files"
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose logging output'
    )
    return parser.parse_args()


def install_keys(server: Server) -> None:
    """Installs the keys for all mods of the server."""

    for mod in chain(server.mods, server.server_mods):
        for key in mod.bikeys(server.base_dir):
            if (installed := server.base_dir / 'keys' / key.name).exists():
                LOGGER.info('Key "%s" already installed.', key.name)
                continue

            with key.open('rb') as src, installed.open('wb') as dst:
                dst.write(src.read())


def fix_mod_paths(server: Server) -> None:
    """Fix paths of the server mods."""

    for mod in server.mods:
        mod.fix_paths(server.base_dir)


def update(server: Server, args: Namespace) -> None:
    """Perform server and mod updates."""

    updater = Updater(args.update)

    if args.update_server:
        updater.update_server(server)
        print()

    if args.update_mods:
        updater.update_mods(server)
        print()


def list_mods(server: Server) -> None:
    """List mods."""

    print_mods(server.mods, header='Mods')

    if server.mods and server.server_mods:
        print()

    print_mods(server.server_mods, header='Server mods')


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

    if args.update:
        update(server, args)

    if args.fix_paths:
        fix_mod_paths(server)

    if args.install_keys:
        install_keys(server)

    if args.list_mods:
        list_mods(server)

    if args.installed_mods:
        print_mods(ModMetadata.list(server.base_dir), header='Installed mods')

    return 0
