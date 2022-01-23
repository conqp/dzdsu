"""Server representation."""

from enum import Enum
from functools import cache
from json import load
from pathlib import Path
from typing import Any, Iterator, NamedTuple

from dzdsu.constants import SERVER_BINARY
from dzdsu.mods import Mod, mods_str, enabled_mods
from dzdsu.params import ServerParams


__all__ = ['ServerType', 'Server', 'load_servers', 'load_servers_json']


class ServerType(Enum):
    """Available server versions."""

    VANILLA = 223350
    EXP = 1042420


class Server(NamedTuple):
    """A server."""

    name: str
    type: ServerType
    base_dir: Path
    mods: list[Mod]
    server_mods: list[Mod]
    params: ServerParams

    @classmethod
    def from_json(cls, name: str, json: dict):
        """Creates a Server instance from a JSON-ish dict."""
        if typ := json.get('type'):
            typ = ServerType(typ)

        if mods := json.get('mods'):
            mods = [Mod.from_json(json) for json in mods]

        if server_mods := json.get('server_mods'):
            mods = [Mod.from_json(json) for json in server_mods]

        params = ServerParams.from_json(json.get('params') or {})

        return cls(
            name,
            typ or ServerType.VANILLA,
            json['base_dir'],
            mods or [],
            server_mods or [],
            params
        )

    def get_binary_args(self) -> Iterator[str]:
        """Yields arguments for the server binary."""
        yield from self.params.get_binary_args()

        if mods := mods_str(enabled_mods(self.mods)):
            yield f'-mod={mods}'

        if mods := mods_str(enabled_mods(self.server_mods)):
            yield f'-serverMod={mods}'

    @property
    def command(self) -> list[str]:
        """Returns the full command for running the server."""
        return [str(Path.cwd() / SERVER_BINARY), *self.get_binary_args()]

    @property
    def app_id(self) -> int:
        """Returns the Steam app ID."""
        return self.type.value


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
