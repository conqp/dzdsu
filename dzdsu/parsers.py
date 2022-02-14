"""Config file parsers."""

from configparser import ConfigParser, SectionProxy
from os import linesep
from re import fullmatch
from tempfile import NamedTemporaryFile
from typing import Iterable, Iterator


__all__ = ['parse_battleye_cfg', 'parse_server_cfg']


def parse_battleye_value(key: str, value: str) -> bool | int | str:
    """Parses a BattlEye config value."""

    if key == 'RConPort':
        return int(value)

    if key == 'RestrictRCon':
        return bool(int(value))

    return value


def parse_battleye_cfg(
        lines: Iterable[str]
) -> Iterator[tuple[str, bool | int | str]]:
    """Yields key / value pairs of the given config file."""

    for line in lines:
        if not (line := line.strip()) or line.startswith('#'):
            continue

        key, value = line.split(maxsplit=1)
        yield key, parse_battleye_value(key, value)


def server_cfg_to_ini(lines: Iterable[str], section: str) -> Iterator[str]:
    """Yields lines of an INI-style representation of the server config."""

    yield f'[{section}]'

    for line in lines:
        if not (line := line.strip()):
            continue

        if not (match := fullmatch(r'^(\w+)\s*=\s*(\w+);.*', line)):
            continue

        yield ' = '.join(match.groups())


def parse_server_cfg(
        lines: Iterable[str], *, section: str = 'Server'
) -> SectionProxy:
    """Yields key / value pairs of the given server config."""

    config = ConfigParser()

    with NamedTemporaryFile('w+b') as file:
        for line in server_cfg_to_ini(lines, section):
            file.write(line)
            file.write(linesep)

        file.flush()
        config.read(file.name)

    return config[section]
