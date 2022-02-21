"""Server backups."""

from argparse import Namespace
from datetime import datetime

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['backup']


def gen_filename(mission: str) -> str:
    """Generates a file name."""

    return f'{mission}-{datetime.now().isoformat()}.tar.gz'


def backup(server: Server, args: Namespace) -> int:
    """Creates a backup of the server."""

    for mission in set(args.mission):
        if (path := args.backup_dir / gen_filename(mission)).exists():
            LOGGER.error('Backup file "%s" already exists.', path)
            return 1

        server.mission(mission).backup(args.backup_dir / gen_filename(mission))

    return 0
