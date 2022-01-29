"""Modifications from the Steam workshop."""

from __future__ import annotations
from pathlib import Path
from typing import Iterable, NamedTuple, Optional, Union

from dzdsu.constants import BOLD
from dzdsu.constants import DAYZ_APP_ID
from dzdsu.constants import ITALIC
from dzdsu.constants import LINK
from dzdsu.constants import MODS_BASE_DIR
from dzdsu.constants import WORKSHOP_URL


__all__ = ['Mod', 'mods_str', 'print_mods']


class Mod(NamedTuple):
    """A server mod."""

    id: int
    name: Optional[str] = None
    enabled: bool = True

    def __str__(self) -> str:
        return LINK.format(url=self.url, text=self.name or self.id)

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

    @property
    def path(self) -> Path:
        """Returns the relative path to the local mod directory."""
        return MODS_BASE_DIR / str(DAYZ_APP_ID) / str(self.id)

    @property
    def url(self) -> str:
        """Returns the Steam Workshop URL."""
        return WORKSHOP_URL.format(self.id)


def mods_str(mods: Iterable[Mod], *, sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(str(mod.path) for mod in mods)


def print_mods(
        mods: Iterable[Mod], *,
        header: str = 'Mods'
) -> None:
    """Lists the respective mods."""

    if not mods:
        return

    print(BOLD.format(header))

    for mod in mods:
        print(mod if mod.enabled else ITALIC.format(mod))
