"""Wiping of servers."""

from dzdsu.utility.logger import LOGGER
from dzdsu.server import Server


__all__ = ['wipe']


def wipe_mission(server: Server, mission: str) -> bool:
    """Wipes a mission on a server."""

    try:
        mission = server.mission(mission)
    except (FileNotFoundError, ValueError) as error:
        LOGGER.error('Invalid mission: %s', mission)
        LOGGER.debug(str(error))
        return False

    mission.wipe()
    return True


def wipe(server: Server, missions: set[str]) -> bool:
    """Wipes a mission on a server."""

    return all({wipe_mission(server, mission) for mission in missions})
