"""Modifications from the Steam workshop."""

from pathlib import Path
from typing import Iterable, Iterator

from dzdsu.constants import DAYZ_APP_ID, MODS_BASE_DIR


__all__ = ['enabled_mods', 'mod_paths', 'mods_str']


def enabled_mods(mods: list[int]) -> Iterator[int]:
    """Yields enabled mods."""

    return filter(lambda mod: mod > 0, mods)


def mod_paths(mods: Iterable[int]) -> Iterator[Path]:
    """Yields mod paths."""

    return map(lambda mod: MODS_BASE_DIR / str(DAYZ_APP_ID) / str(mod), mods)


def mods_str(mods: Iterable[int], *, sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(map(str, mod_paths(mods)))

