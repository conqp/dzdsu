"""Server representation."""

from enum import Enum
from functools import cache
from json import load
from pathlib import Path
from typing import NamedTuple

from dzdsu.mods import Mod


__all__ = ['ServerType', 'Server', 'load_servers', 'load_servers_json']


class ServerType(Enum):
    """Available server versions."""

    VANILLA = 223350
    EXP = 1042420

    def __int__(self):
        return self.value


class Server(NamedTuple):
    """A server."""

    type: ServerType
    base_dir: Path
    mods: set[Mod]

    @classmethod
    def from_json(cls, json: dict):
        """Creates a Server instance from a JSON-ish dict."""
        if typ := json.get('type'):
            typ = ServerType(typ)

        if mods := json.get('mods'):
            mods = {Mod.from_json(json) for json in mods}

        return cls(typ or ServerType.VANILLA, json['base_dir'], mods or set())

    @property
    def app_id(self) -> int:
        """Returns the Steam app ID."""
        return int(self.type)


def load_servers(file: Path) -> list[Server]:
    """Loads servers."""

    return [Server.from_json(json) for json in load_servers_json(file)]


@cache
def load_servers_json(file: Path) -> list[dict]:
    """Loads servers from a JSON file."""

    with file.open('r') as json:
        return load(json)
