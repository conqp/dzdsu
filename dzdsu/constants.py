"""Common constants."""

from os import getenv, name
from pathlib import Path


__all__ = [
    'BATTLEYE_GLOB',
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'ITALIC',
    'JSON_FILE',
    'LINK',
    'MESSAGE_TEMPLATE_SHUTDOWN',
    'MESSAGE_TEMPLATE_UPDATE',
    'MODS_BASE_DIR',
    'MODS_DIR',
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
MODS_BASE_DIR = Path('steamapps/workshop/content/')
MODS_DIR = MODS_BASE_DIR / str(DAYZ_APP_ID)
UNSUPPORTED_OS = OSError('Unsupported operating system.')
STEAMCMD = 'steamcmd'
WORKSHOP_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'

ITALIC = '\033[3m{}\033[0m'
LINK = '\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\'

if name == 'nt':
    JSON_FILE = Path(getenv('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    SERVER_EXECUTABLE = 'DayZServer_x64.exe'
elif name == 'posix':
    JSON_FILE = Path('/etc/dzservers.json')
    SERVER_EXECUTABLE = 'DayZServer'
else:
    raise UNSUPPORTED_OS
