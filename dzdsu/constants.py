"""Common constants."""

from os import name


__all__ = ['CONFIG_FILE', 'SERVER_BINARY', 'STEAMCMD']


CONFIG_FILE = 'serverDZ.cfg'

if name == 'nt':
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')


STEAMCMD = 'steamcmd'
