"""Modifications from the Steam workshop."""

from __future__ import annotations
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple, Optional, Union

from dzdsu.constants import DAYZ_APP_ID, MODS_BASE_DIR, MOD_NAMES


__all__ = [
    'Mod',
    'mod_paths',
    'mods_str',
    'print_mods'
]


class Mod(NamedTuple):
    """A server mod."""

    id: int
    name: Optional[str] = None
    enabled: bool = True

    def __str__(self) -> str:
        return str(self.id) if self.name is None else self.name

    @classmethod
    def from_int(cls, integer: int, *, name: Optional[str] = None) -> Mod:
        """Creates a mod from an integer."""
        if integer == 0:
            raise ValueError(f'Invalid mod ID: {integer}')

        if integer < 0:
            return cls(abs(integer), name, enabled=False)

        return cls(integer, name)

    @classmethod
    def from_json(cls, json: dict[str, Union[int, str]]) -> Mod:
        """Creates a mod from a JSON-ish dict."""
        return cls.from_int(json['id'], name=json.get('name'))

    @classmethod
    def from_value(cls, value: Union[int, dict[str, Union[int, str]]]) -> Mod:
        """Creates a mod from an int or JSON value."""
        if isinstance(value, int):
            return cls.from_int(value)

        if isinstance(value, dict):
            return cls.from_json(value)

        raise TypeError(f'Cannot create mod from: {value} ({type(value)})')


def mod_paths(mods: Iterable[Mod]) -> Iterator[Path]:
    """Yields mod paths."""

    return map(lambda mod: MODS_BASE_DIR / f'{DAYZ_APP_ID}/{mod.id}', mods)


def mods_str(mods: Iterable[Mod], *, sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(map(str, mod_paths(mods)))


def print_mods(
        mods: Iterable[Mod], *,
        prefix: str = 'Mod:'
) -> None:
    """Lists the respective mods."""

    for mod in mods:
        print(prefix, mod)
