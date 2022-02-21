"""Main script of the server management utility."""

from logging import DEBUG, INFO, WARNING, basicConfig

from dzdsu.constants import MESSAGE_TEMPLATE_SHUTDOWN
from dzdsu.mods import print_mods
from dzdsu.server import load_servers
from dzdsu.utility.argparse import get_args
from dzdsu.utility.backup import backup
from dzdsu.utility.logger import LOGGER
from dzdsu.utility.mods import clean_mods, fix_mod_paths, install_keys
from dzdsu.utility.shutdown import shutdown
from dzdsu.utility.update import update
from dzdsu.utility.wipe import wipe


__all__ = ['main']


def main() -> int:
    """Server management utility."""

    args = get_args(__doc__)
    basicConfig(level=DEBUG if args.debug else WARNING if args.quiet else INFO)
    servers = load_servers(args.servers_file)

    try:
        server = servers[args.server]
    except KeyError:
        LOGGER.error('No such server: %s', args.server)
        return 2

    if args.clean_mods:
        clean_mods(server)

    if args.update:
        update(server, args)

    if args.fix_paths:
        fix_mod_paths(server)

    if args.install_keys:
        install_keys(server, overwrite=args.overwrite)

    if args.list_mods:
        print_mods(server.mods)

    if args.list_server_mods:
        print_mods(server.server_mods)

    if args.installed_mods:
        print_mods(sorted(map(
            lambda installed_mod: installed_mod.mod, server.installed_mods
        )))

    if args.shutdown and not shutdown(
        server,
        args.message or MESSAGE_TEMPLATE_SHUTDOWN,
        args.countdown
    ):
        return 3

    if args.backup and not backup(server, set(args.backup), args.backups_dir):
        return 4

    if args.wipe and not wipe(server, set(args.wipe)):
        return 5

    if args.needs_restart and not server.needs_restart:
        return 1

    return 0
