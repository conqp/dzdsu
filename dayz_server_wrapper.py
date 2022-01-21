#! /usr/bin/env python3
"""DayZ server wrapper."""

from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from os import name
from pathlib import Path
from subprocess import run
from sys import exit
from typing import Iterator


CONFIG_FILE = Path('dayz.ini')

if name == 'nt':
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-f', '--config-file', type=Path, default=CONFIG_FILE, metavar='file',
        help='config file path'
    )
    return parser.parse_args()


def get_mods(config: ConfigParser) -> Iterator[str]:
    """Yield enabled mods."""

    if not config.has_section('mods'):
        return

    for mod in config.options('mods'):
        if config.getboolean('mods', mod):
            if not mod.startswith('@'):
                yield f'@{mod}'
            else:
                yield mod


def get_parameters(config: ConfigParser) -> Iterator[str]:
    """Yields arguments for the DayZ server.
    INI file structure:

    [logging]
    adminlog = (on|off)
    netlog = (on|off)

    [security]
    srcAllowFileWrite = (on|off)
    noFilePatching = (on|off)
    freezecheck = (on|off)

    [server]
    instanceId = <int|0=disabled>
    config = <file_name>
    port = <int>
    profiles = <dir_name>

    [mods]
    <mod_name1> = (on|off)
    <mod_name2> = (on|off)
    ...
    """

    if config.getboolean('logging', 'adminlog', fallback=True):
        yield '-adminlog'

    if config.getboolean('logging', 'netlog', fallback=True):
        yield '-netlog'

    if config.getboolean('security', 'srcAllowFileWrite', fallback=True):
        yield '-srcAllowFileWrite'

    if config.getboolean('security', 'noFilePatching', fallback=True):
        yield '-noFilePatching'

    if config.getboolean('security', 'freezecheck', fallback=True):
        yield '-freezecheck'

    if instance_id := config.getint('server', 'instanceId', fallback=1):
        yield f'-instanceId={instance_id}'

    if config_file := config.get('server', 'config', fallback='serverDZ.cfg'):
        yield f'-config={config_file}'

    if port := config.getint('server', 'port', fallback=2302):
        yield f'-port={port}'

    if profiles := config.get('server', 'profiles', fallback='ServerProfiles'):
        yield f'-profiles={profiles}'

    if mods := list(get_mods(config)):
        yield f'-mods={";".join(mods)}'


def main() -> int:
    """Starts the DayZ server."""

    args = get_args()
    config = ConfigParser()
    config.read(args.config_file)
    binary = Path.cwd() / SERVER_BINARY
    command = [str(binary), *get_parameters(config)]
    completed_process = run(command, check=False)
    return completed_process.returncode


if __name__ == '__main__':
    exit(main())
