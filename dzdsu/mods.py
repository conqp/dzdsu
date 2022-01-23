"""Modifications from the Steam workshop."""

from functools import cache
from json import load
from pathlib import Path
from typing import Iterable, Iterator

from dzdsu.constants import DAYZ_APP_ID, MODS_BASE_DIR, MOD_NAMES


__all__ = [
    'enabled_mods',
    'list_mods',
    'load_mod_names',
    'mod_paths',
    'mods_str'
]


def enabled_mods(mods: list[int]) -> Iterator[int]:
    """Yields enabled mods."""

    return filter(lambda mod: mod > 0, mods)


def get_mod_name(mod: int, *, file: Path = MOD_NAMES) -> str:
    """Returns the mod name."""

    try:
        return load_mod_names(file)[mod]
    except KeyError:
        return str(mod)


def list_mods(
        mods: Iterable[int], *,
        prefix: str = 'Mod:',
        file: Path = MOD_NAMES
) -> None:
    """Lists the respective mods."""

    for mod in mods:
        print(prefix, get_mod_name(mod, file=file))


@cache
def load_mod_names(file: Path) -> dict[int, str]:
    """Loads mod names from the given file."""

    try:
        with file.open('r') as json:
            mods = load(json)
    except FileNotFoundError:
        return {}

    return {ident: name for name, ident in mods.items()}


def mod_paths(mods: Iterable[int]) -> Iterator[Path]:
    """Yields mod paths."""

    return map(lambda mod: MODS_BASE_DIR / str(DAYZ_APP_ID) / str(mod), mods)


def mods_str(mods: Iterable[int], *, sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(map(str, mod_paths(mods)))
