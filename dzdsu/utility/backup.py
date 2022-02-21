"""Server backups."""

from argparse import Namespace
from datetime import datetime

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['backup']


def gen_filename(server: Server, mission: str) -> str:
    """Generates a file name."""

    return f'{server.name}-{mission}-{datetime.now().isoformat()}.tar.gz'


def backup(server: Server, args: Namespace) -> int:
    """Creates a backup of the server."""

    for mission in set(args.mission):
        if (file := args.backup_dir / gen_filename(server, mission)).exists():
            LOGGER.error('Backup file "%s" already exists.', file)
            return 1

        server.mission(mission).backup(file)

    return 0
