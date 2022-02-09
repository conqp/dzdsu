"""Modifications from the Steam workshop."""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple, Optional, Union

from dzdsu.constants import BOLD
from dzdsu.constants import DAYZ_APP_ID
from dzdsu.constants import ITALIC
from dzdsu.constants import LINK
from dzdsu.constants import MODS_BASE_DIR
from dzdsu.constants import WORKSHOP_URL


__all__ = ['Mod', 'ModMetadata', 'mods_str', 'print_mods']


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
    def url(self) -> str:
        """Returns the Steam Workshop URL."""
        return WORKSHOP_URL.format(self.id)

    @property
    def path(self) -> Path:
        """Returns the relative path to the local mod directory."""
        return MODS_BASE_DIR / str(DAYZ_APP_ID) / str(self.id)

    @property
    def addons(self) -> Path:
        """Returns the relative path to the addons directory."""
        return self.path / 'addons'

    @property
    def keys(self) -> Path:
        """Returns the relative path to the keys directory."""
        return self.path / 'keys'

    def pbos(self, base_dir: Path) -> Iterator[Path]:
        """Yields absolute paths to .pbo files."""
        return (base_dir / self.addons).glob('*.pbo')

    def bikeys(self, base_dir: Path) -> Iterator[Path]:
        """Yields absolute path to the *.bikey files."""
        return (base_dir / self.keys).glob('*.bikey')

    def fix_paths(self, base_dir: Path) -> None:
        """Links paths to lower-case."""
        if (addons := base_dir / self.path / 'Addons').is_dir():
            link_to_lowercase(addons)

        if (keys := base_dir / self.path / 'Keys').is_dir():
            link_to_lowercase(keys)

        for pbo in self.pbos(base_dir):
            link_to_lowercase(pbo)


class ModMetadata(NamedTuple):
    """Metadata of a mod."""

    protocol: int
    publishedid: int
    name: str
    timestamp: datetime

    def __str__(self) -> str:
        return LINK.format(url=self.url, text=self.name)

    @property
    def url(self) -> str:
        """Returns the Steam Workshop URL."""
        return WORKSHOP_URL.format(self.publishedid)

    @classmethod
    def from_dict(cls, dct: dict) -> ModMetadata:
        """Creates mod metadata from the given dict."""
        return cls(
            int(dct['protocol']),
            int(dct['publishedid']),
            dct['name'].strip('"'),
            datetime.fromtimestamp(int(dct['timestamp']))
        )

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> ModMetadata:
        """Creates mod metadata from the given lines."""
        return cls.from_dict({
            key: value.rstrip(';') for key, value in (
                line.split(' = ') for line in (
                    line.strip() for line in lines
                ) if line
            )
        })

    @classmethod
    def from_file(cls, filename: Path) -> ModMetadata:
        """Reads the mod metadata from the given file."""
        with filename.open('r', encoding='utf-8') as file:
            return cls.from_lines(file)

    @classmethod
    def list(cls, base_dir: Path) -> Iterator[ModMetadata]:
        """Yields installed mod metadata."""
        mods_dir = base_dir / MODS_BASE_DIR / str(DAYZ_APP_ID)

        for filename in mods_dir.glob('*/meta.cpp'):
            yield cls.from_file(filename)


def link_to_lowercase(path: Path) -> None:
    """Creates a symlink with the path names in lower case."""

    if (filename := path.name) == (lower := filename.lower()):
        return

    if (symlink := path.parent / lower).exists():
        return

    symlink.symlink_to(filename)


def mods_str(mods: Iterable[Mod], sep: str = ';') -> str:
    """Returns a string representation of the given mods."""

    return sep.join(str(mod.path) for mod in mods)


def print_mods(
        mods: Iterable[Mod | ModMetadata], *,
        header: str = 'Mods'
) -> None:
    """Lists the respective mods."""

    if not mods:
        return

    print(BOLD.format(header))

    for mod in mods:
        print(mod if mod.enabled else ITALIC.format(mod))
