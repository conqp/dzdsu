"""Common constants."""

from os import getenv, name
from pathlib import Path


__all__ = [
    'BATTLEYE_GLOB',
    'BACKUPS_DIR',
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'ITALIC',
    'JSON_FILE',
    'LINK',
    'MESSAGE_TEMPLATE_SHUTDOWN',
    'MESSAGE_TEMPLATE_UPDATE',
    'MODS_DIR',
    'PROCESS_NAME',
    'SERVER_EXECUTABLE',
    'STEAMCMD',
    'UNSUPPORTED_OS',
    'WORKSHOP_URL'
]


BATTLEYE_GLOB = 'beserver_x64*.cfg'
CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
MESSAGE_TEMPLATE_SHUTDOWN = 'Server is going down for maintenance in {}!'
MESSAGE_TEMPLATE_UPDATE = 'Server is going down for updates in {}!'
MODS_DIR = Path('steamapps/workshop/content') / str(DAYZ_APP_ID)
UNSUPPORTED_OS = OSError('Unsupported operating system.')
STEAMCMD = 'steamcmd'
WORKSHOP_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'

ITALIC = '\033[3m{}\033[0m'
LINK = '\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\'

if name == 'nt':
    _CONFIG_DIR = Path(getenv('PROGRAMFILES')) / 'dzsrv'
    BACKUPS_DIR = _CONFIG_DIR / 'backups'
    JSON_FILE = _CONFIG_DIR / 'servers.json'
    PROCESS_NAME = SERVER_EXECUTABLE = 'DayZServer_x64.exe'
elif name == 'posix':
    BACKUPS_DIR = Path('/var/lib/dzbackups')
    JSON_FILE = Path('/etc/dzservers.json')
    PROCESS_NAME = 'enfMain'
    SERVER_EXECUTABLE = 'DayZServer'
else:
    raise UNSUPPORTED_OS
