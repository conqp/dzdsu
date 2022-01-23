"""Modifications from the Steam workshop."""

from typing import Iterable, Iterator, NamedTuple


__all__ = ['Mod', 'enabled_mods', 'mod_names', 'mods_str']


class Mod(NamedTuple):
    """Represents a mod."""

    id: int
    name: str
    disabled: bool = False

    @classmethod
    def from_json(cls, json: dict):
        """Creates an instance of Mod from a JSON-ish dict."""
        return cls(json['id'], json['name'], json.get('disabled', False))


def enabled_mods(mods: list[Mod]) -> Iterator[Mod]:
    """Yields enabled mods."""

    return filter(lambda mod: mod.enabled, mods)


def mod_names(mods: Iterable[Mod]) -> Iterator[str]:
    """Yields names mods."""

    return map(lambda mod: mod.name, mods)


def mods_str(mods: Iterable[Mod], *, sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(mod_names(mods))

