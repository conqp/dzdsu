"""Common constants."""

from os import environ, name
from pathlib import Path


__all__ = [
    'ADDONS_GLOB',
    'BOLD',
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'ITALIC',
    'JSON_FILE',
    'KEYS_DIR_GLOB',
    'KEYS_GLOB',
    'LINK',
    'MODS_BASE_DIR',
    'PBO_GLOB',
    'SERVER_BINARY',
    'STEAMCMD',
    'WORKSHOP_URL'
]


ADDONS_GLOB = '[Aa]ddons'
CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
KEYS_DIR_GLOB = '[Kk]eys'
KEYS_GLOB = f'{DAYZ_APP_ID}/*/{KEYS_DIR_GLOB}/*.bikey'
MODS_BASE_DIR = Path('steamapps/workshop/content/')
PBO_GLOB = '*.pbo'
STEAMCMD = 'steamcmd'
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
