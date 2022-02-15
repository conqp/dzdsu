"""Server representation."""

from configparser import SectionProxy
from itertools import chain
from json import load
from pathlib import Path
from typing import Any, Iterator, NamedTuple

from dzdsu.constants import BATTLEYE_GLOB
from dzdsu.constants import DAYZ_SERVER_APP_ID
from dzdsu.constants import JSON_FILE
from dzdsu.constants import MODS_DIR
from dzdsu.constants import SERVER_EXECUTABLE
from dzdsu.mods import Mod, ModMetadata, InstalledMod, mods_str
from dzdsu.params import ServerParams
from dzdsu.parsers import parse_battleye_cfg, parse_server_cfg


__all__ = ['Server', 'load_servers']


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

    @property
    def executable(self) -> Path:
        """Returns the absolute path to the server's executable file."""
        return self.base_dir / SERVER_EXECUTABLE

    @property
    def executable_args(self) -> Iterator[str]:
        """Yields arguments for the server executable."""
        yield from self.params.executable_args

        if mods := mods_str(mod for mod in self.mods if mod.enabled):
            yield f'-mod={mods}'

        if mods := mods_str(mod for mod in self.server_mods if mod.enabled):
            yield f'-serverMod={mods}'

    @property
    def command(self) -> list[str]:
        """Returns the full command for running the server."""
        return [str(self.executable), *self.executable_args]

    @property
    def mods_dir(self) -> Path:
        """Returns the server's mods directory."""
        return self.base_dir / MODS_DIR

    @property
    def battleye_cfg_file(self) -> Path:
        """Returns the BattlEye RCon config file."""
        for path in self.base_dir.glob(BATTLEYE_GLOB):
            if path.is_file():
                return path

        raise FileNotFoundError(BATTLEYE_GLOB)

    @property
    def battleye_cfg(self) -> dict[str, str | int | bool]:
        """Returns the BattlEye RCon configuration."""
        with self.battleye_cfg_file.open('r', encoding='utf-8') as file:
            return dict(parse_battleye_cfg(file))

    @property
    def installed_mods_metadata(self) -> Iterator[ModMetadata]:
        """Yields metadata of installed mods."""
        for filename in self.mods_dir.glob('*/meta.cpp'):
            yield ModMetadata.from_file(filename)

    @property
    def config_file(self) -> Path:
        """Returns the config file path."""
        return self.base_dir / 'serverDZ.cfg'

    @property
    def config(self) -> SectionProxy:
        """Returns the configuration settings."""
        with self.config_file.open('r', encoding='utf-8') as file:
            return parse_server_cfg(file)

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


def load_servers_json(file: Path) -> dict[str, Any]:
    """Loads servers from a JSON file."""

    with file.open('r') as json:
        return load(json)


def load_servers(file: Path = JSON_FILE) -> dict[str, Server]:
    """Loads servers."""

    return {
        name: Server.from_json(name, json)
        for name, json in load_servers_json(file).items()
    }
