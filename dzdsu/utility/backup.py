"""Server backups."""

from datetime import datetime
from pathlib import Path
from typing import Iterable

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['backup']


def gen_filename(server: Server, mission: str) -> str:
    """Generates a file name."""

    return f'{server.name}-{mission}-{datetime.now().isoformat()}.tar.gz'


def backup_mission(server: Server, mission: str, backups_dir: Path) -> bool:
    """Creates a backup of a single mission."""

    if (file := backups_dir / gen_filename(server, mission)).exists():
        LOGGER.error('Backup file "%s" already exists.', file)
        return False

    try:
        mission = server.mission(mission)
    except (FileNotFoundError, ValueError) as error:
        LOGGER.error(error)
        return False

    mission.backup(file)
    return True


def backup(server: Server, missions: set[str], backups_dir: Path) -> bool:
    """Creates a backup of the server."""

    return all({
        backup_mission(server, mission, backups_dir) for mission in missions
    })
