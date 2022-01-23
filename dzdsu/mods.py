"""Modifications from the Steam workshop."""

from functools import cache
from json import load
from pathlib import Path
from typing import NamedTuple


__all__ = ['Mod', 'load_mods', 'load_mods_json']


class Mod(NamedTuple):
    """Represents a mod."""

    id: int
    name: str

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name


@cache
def load_mods(file: Path) -> set[Mod]:
    """Loads mods as a set of Mod objects."""

    return {Mod(ident, name) for ident, name in load_mods_json(file).items()}


@cache
def load_mods_json(file: Path) -> dict[int, str]:
    """Loads the mods from a JSON file."""

    with file.open('r') as json:
        return load(json)
