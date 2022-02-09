"""Server representation."""

from functools import cache
from itertools import chain
from json import load
from pathlib import Path
from typing import Any, Iterator, NamedTuple

from dzdsu.constants import DAYZ_SERVER_APP_ID, MODS_DIR, SERVER_BINARY
from dzdsu.mods import Mod, ModMetadata, InstalledMod, mods_str
from dzdsu.params import ServerParams


__all__ = ['Server', 'load_servers', 'load_servers_json']


class Server(NamedTuple):
    """A server."""

    name: str
    app_id: int
    base_dir: Path
    mods: list[Mod]
    server_mods: list[Mod]
    params: ServerParams

    @classmethod
    def from_json(cls, name: str, json: dict):
        """Creates a Server instance from a JSON-ish dict."""
        return cls(
            name,
            json.get('appId', DAYZ_SERVER_APP_ID),
            Path(json['basedir']),
            [Mod.from_value(mod) for mod in (json.get('mods') or [])],
            [Mod.from_value(mod) for mod in (json.get('serverMods') or [])],
            ServerParams.from_json(json.get('params') or {})
        )

    def get_binary_args(self) -> Iterator[str]:
        """Yields arguments for the server binary."""
        yield from self.params.get_binary_args()

        if mods := mods_str(mod for mod in self.mods if mod.enabled):
            yield f'-mod={mods}'

        if mods := mods_str(mod for mod in self.server_mods if mod.enabled):
            yield f'-serverMod={mods}'

    @property
    def command(self) -> list[str]:
        """Returns the full command for running the server."""
        return [str(self.base_dir / SERVER_BINARY), *self.get_binary_args()]

    @property
    def mods_dir(self) -> Path:
        """Returns the server's mods directory."""
        return self.base_dir / MODS_DIR

    @property
    def installed_mods_metadata(self) -> Iterator[ModMetadata]:
        """Yields metadata of installed mods."""
        for filename in self.mods_dir.glob('*/meta.cpp'):
            yield ModMetadata.from_file(filename)

    @property
    def installed_mods(self) -> Iterator[InstalledMod]:
        """Yields installed mods."""
        for meta in self.installed_mods_metadata:
            yield InstalledMod(meta.publishedid, self.base_dir)

    @property
    def used_mods(self) -> Iterator[Mod]:
        """Yields used mods."""
        return chain(self.mods, self.server_mods)

    @property
    def unused_mods(self) -> Iterator[InstalledMod]:
        """Yields unused mods."""
        used_ids = {mod.id for mod in self.used_mods}

        for meta in self.installed_mods_metadata:
            if meta.publishedid not in used_ids:
                yield InstalledMod(meta.publishedid, self.base_dir)


def load_servers(file: Path) -> dict[str, Server]:
    """Loads servers."""

    return {
        name: Server.from_json(name, json)
        for name, json in load_servers_json(file).items()
    }


@cache
def load_servers_json(file: Path) -> dict[str, Any]:
    """Loads servers from a JSON file."""

    with file.open('r') as json:
        return load(json)
