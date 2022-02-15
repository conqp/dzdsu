"""Common constants."""

from os import environ, name
from pathlib import Path


__all__ = [
    'BATTLEYE_GLOB',
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'ITALIC',
    'JSON_FILE',
    'LINK',
    'MODS_BASE_DIR',
    'MODS_DIR',
    'SERVER_EXECUTABLE',
    'SERVER_EXECUTABLE_WIN',
    'STEAMCMD',
    'STEAMCMD_WINE',
    'WINE',
    'WORKSHOP_URL',
    'XVFB'
]


BATTLEYE_GLOB = 'battleye/beserver_x64*.cfg'
CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
MODS_BASE_DIR = Path('steamapps/workshop/content/')
MODS_DIR = MODS_BASE_DIR / str(DAYZ_APP_ID)
SERVER_EXECUTABLE_WIN = 'DayZServer_x64.exe'
STEAMCMD = 'steamcmd'
STEAMCMD_WINE = '.steamcmd/steamcmd.exe'
WINE = '/usr/bin/wine'
WORKSHOP_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'
XVFB = ('/usr/bin/Xvfb', ':0', '-screen', '0', '1024x768x16')

ITALIC = '\033[3m{}\033[0m'
LINK = '\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\'

if name == 'nt':
    JSON_FILE = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    SERVER_EXECUTABLE = SERVER_EXECUTABLE_WIN
elif name == 'posix':
    JSON_FILE = Path('/etc/dzservers.json')
    SERVER_EXECUTABLE = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')
