"""Server representation."""

from functools import cache
from json import load
from pathlib import Path
from typing import NamedTuple

from dzdsu.emuerations import ServerType
from dzdsu.mods import Mod


__all__ = ['Server', 'load_servers', 'load_servers_json']


class Server(NamedTuple):
    """A server."""

    type: ServerType
    base_dir: Path
    mods: set[Mod]

    @classmethod
    def from_json(cls, json: dict):
        """Creates a Server instance from a JSON-ish dict."""
        if mods := json.get('mods'):
            mods = {Mod(ident, name) for ident, name in mods.items()}

        return cls(ServerType(json['type']), json['base_dir'], mods or set())


def load_servers(file: Path) -> list[Server]:
    """Loads servers."""

    return [Server.from_json(json) for json in load_servers_json(file)]


@cache
def load_servers_json(file: Path) -> list[dict]:
    """Loads servers from a JSON file."""

    with file.open('r') as json:
        return load(json)
