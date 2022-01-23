"""Common constants."""

from os import environ, name
from pathlib import Path


__all__ = [
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'JSON_FILE',
    'KEYS_GLOB',
    'MODS_BASE_DIR',
    'MOD_NAMES',
    'SERVER_BINARY',
    'STEAMCMD'
]


CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
KEYS_GLOB = '@*/[Kk]eys/*.bikey'
MODS_BASE_DIR = Path('steamapps/workshop/content/')

if name == 'nt':
    JSON_FILE = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    MOD_NAMES = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'mods.json'
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    JSON_FILE = Path('/etc/dzservers.json')
    MOD_NAMES = Path('/etc/dzmods.json')
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')


STEAMCMD = 'steamcmd'
