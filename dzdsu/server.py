"""Server representation."""

from functools import cache
from json import load
from pathlib import Path
from typing import Any, Iterator, NamedTuple

from dzdsu.constants import DAYZ_SERVER_APP_ID, SERVER_BINARY
from dzdsu.mods import Mod, mods_str
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
            json.get('app_id', DAYZ_SERVER_APP_ID),
            Path(json['base_dir']),
            [Mod.from_value(mod) for mod in (json.get('mods') or [])],
            [Mod.from_value(mod) for mod in (json.get('server_mods') or [])],
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
