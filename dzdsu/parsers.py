"""Config file parsers."""

from configparser import ConfigParser, SectionProxy
from re import fullmatch
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


def server_cfg_to_ini(lines: Iterable[str]) -> Iterator[tuple[str, str]]:
    """Yields lines of an INI-style representation of the server config."""

    for line in lines:
        if not (line := line.strip()):
            continue

        if not (match := fullmatch(r'^(\w+)\s*=\s*(.+);.*', line)):
            continue

        key, value = match.groups()
        yield key, value.strip('"')


def parse_server_cfg(
        lines: Iterable[str], *, section: str = 'Server'
) -> SectionProxy:
    """Yields key / value pairs of the given server config."""

    config = ConfigParser()
    config.read_dict({section: dict(server_cfg_to_ini(lines))})
    return config[section]
