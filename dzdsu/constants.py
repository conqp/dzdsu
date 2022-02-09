"""Common constants."""

from datetime import datetime
from os import environ, name
from pathlib import Path


__all__ = [
    'BOLD',
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'ITALIC',
    'JSON_FILE',
    'LINK',
    'MODS_BASE_DIR',
    'MODS_DIR',
    'SERVER_BINARY',
    'STEAMCMD',
    'TIMESTAMP_OFFSET',
    'WORKSHOP_URL'
]


CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
MODS_BASE_DIR = Path('steamapps/workshop/content/')
MODS_DIR = MODS_BASE_DIR / str(DAYZ_APP_ID)
STEAMCMD = 'steamcmd'
TIMESTAMP_OFFSET = datetime(311, 9, 19, 21, 9, 1, 300000)   # Some magic here.
WORKSHOP_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'

BOLD = '\033[1m{}\033[0m'
ITALIC = '\033[3m{}\033[0m'
LINK = '\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\'

if name == 'nt':
    JSON_FILE = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    JSON_FILE = Path('/etc/dzservers.json')
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')
