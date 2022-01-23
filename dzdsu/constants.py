"""Common constants."""

from os import environ, name
from pathlib import Path


__all__ = [
    'CONFIG_FILE',
    'JSON_FILE',
    'KEYS_GLOB',
    'SERVER_BINARY',
    'STEAMCMD'
]


CONFIG_FILE = 'serverDZ.cfg'
KEYS_GLOB = '@*/[Kk]eys/*.bikey'

if name == 'nt':
    JSON_FILE = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    JSON_FILE = Path('/etc/servers.json')
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')


STEAMCMD = 'steamcmd'
