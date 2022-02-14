"""Config file parsers."""

from typing import Iterable, Iterator


__all__ = ['parse_battleye_cfg']


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
