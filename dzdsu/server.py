"""Server representation."""

from functools import cache
from json import load
from pathlib import Path
from typing import Any, Iterable, Iterator, NamedTuple

from dzdsu.constants import DAYZ_SERVER_APP_ID, SERVER_BINARY
from dzdsu.mods import Mod
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

    def mods_str(self, mods: Iterable[Mod], sep: str = ';') -> str:
        """Returns a string representation of the given mods."""
        return sep.join(str(mod.path(self.base_dir)) for mod in mods)

    def get_binary_args(self) -> Iterator[str]:
        """Yields arguments for the server binary."""
        yield from self.params.get_binary_args()

        if mods := self.mods_str(mod for mod in self.mods if mod.enabled):
            yield f'-mod={mods}'

        if mods := self.mods_str(
                mod for mod in self.server_mods if mod.enabled
        ):
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
