"""Server backups."""

from datetime import datetime
from os import name
from pathlib import Path

from dzdsu.server import Server
from dzdsu.utility.logger import LOGGER


__all__ = ['backup']


def gen_filename(server: Server, mission: str) -> str:
    """Generates a file name."""

    timestamp = datetime.now().isoformat()
    filename = f'{server.name}-{mission}-{timestamp}.tar.gz'

    if name == 'nt':
        return filename.replace(":", "_")

    return filename


def backup_mission(server: Server, mission: str, backups_dir: Path) -> bool:
    """Creates a backup of a single mission."""

    if (file := backups_dir / gen_filename(server, mission)).exists():
        LOGGER.error('Backup file "%s" already exists.', file)
        return False

    try:
        mission = server.mission(mission)
    except (FileNotFoundError, ValueError) as error:
        LOGGER.error('Invalid mission: %s', mission)
        LOGGER.debug(str(error))
        return False

    mission.backup(file)
    return True


def backup(server: Server, missions: set[str], backups_dir: Path) -> bool:
    """Creates a backup of the server."""

    try:
        backups_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        LOGGER.error('Cannot create backup directory: %s', backups_dir)
        return False

    return all({
        backup_mission(server, mission, backups_dir) for mission in missions
    })
