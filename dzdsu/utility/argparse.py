"""CLI argument parsing."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from dzdsu.constants import BACKUPS_DIR, JSON_FILE


__all__ = ['get_args']


def get_args(description: str) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument('server', help='the server to operate on')
    parser.add_argument(
        '-f', '--servers-file', type=Path, default=JSON_FILE, metavar='file',
        help='servers JSON file path'
    )
    parser.add_argument(
        '-C', '--clean-mods', action='store_true', help='remove unused mods'
    )
    parser.add_argument(
        '-U', '--update', metavar='steam_user',
        help='update server and/or mods'
    )
    parser.add_argument(
        '-s', '--update-server', action='store_true', help='update server'
    )
    parser.add_argument(
        '-m', '--update-mods', action='store_true',
        help="update the server's mods"
    )
    parser.add_argument(
        '-F', '--fix-paths', action='store_true', help='fix mod file paths'
    )
    parser.add_argument(
        '-K', '--install-keys', action='store_true', help='install mod keys'
    )
    parser.add_argument(
        '--overwrite', action='store_true', help='overwrite existing key files'
    )
    parser.add_argument(
        '-M', '--list-mods', action='store_true', help="list the server's mods"
    )
    parser.add_argument(
        '-S', '--list-server-mods', action='store_true',
        help="list the server's server mods"
    )
    parser.add_argument(
        '-I', '--installed-mods', action='store_true',
        help='list installed mods'
    )
    parser.add_argument(
        '-T', '--shutdown', action='store_true',
        help="shutdown the server if it needs a restart"
    )
    parser.add_argument(
        '-B', '--backup', nargs='*', metavar='mission',
        help='backup the server'
    )
    parser.add_argument(
        '-W', '--wipe', nargs='*', metavar='mission', help='wipe the server'
    )
    parser.add_argument(
        '-N', '--needs-restart', action='store_true',
        help="check whether the server needs a restart"
    )
    parser.add_argument(
        '-b', '--backups-dir', type=Path, default=BACKUPS_DIR, metavar='path',
        help='path to directory containing the backups'
    )
    parser.add_argument(
        '-e', '--message', metavar='template',
        help='RCon countdown message template'
    )
    parser.add_argument(
        '-t', '--countdown', type=int, default=120, metavar='seconds',
        help='countdown time'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', help='show debug messages'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true', help='suppress info messages'
    )
    parser.add_argument('--force', action='store_true', help='force update')
    return parser.parse_args()
