"""Server representation."""

from __future__ import annotations
from configparser import SectionProxy
from hashlib import sha1
from itertools import chain
from json import dump, load
from pathlib import Path
from typing import Any, Iterator, NamedTuple

from dzdsu.constants import BATTLEYE_GLOB
from dzdsu.constants import DAYZ_SERVER_APP_ID
from dzdsu.constants import JSON_FILE
from dzdsu.constants import MODS_DIR
from dzdsu.constants import SERVER_EXECUTABLE
from dzdsu.hash import hash_changed
from dzdsu.lockfile import LockFile
from dzdsu.mods import Mod, ModMetadata, InstalledMod, mods_str
from dzdsu.params import ServerParams
from dzdsu.parsers import parse_battleye_cfg, parse_server_cfg
from dzdsu.rcon import Client


__all__ = ['Server', 'load_servers']


class Server(NamedTuple):
    """A server."""

    name: str
    app_id: int
    base_dir: Path
    executable: Path
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
            Path(json.get('executable', SERVER_EXECUTABLE)),
            [Mod.from_value(mod) for mod in (json.get('mods') or [])],
            [Mod.from_value(mod) for mod in (json.get('serverMods') or [])],
            ServerParams.from_json(json.get('params') or {})
        )

    @property
    def executable_path(self) -> Path:
        """Returns the full command for running the server."""
        if self.executable.is_absolute():
            return self.executable

        return self.base_dir / self.executable

    @property
    def sha1sum(self) -> str:
        """Returns the SHA-1 checksum."""
        with self.executable_path.open('rb') as file:
            return sha1(file.read()).hexdigest()

    @property
    def executable_args(self) -> Iterator[str]:
        """Yields arguments for the server executable."""
        yield from self.params.executable_args
        yield f'-BEpath={self.battleye_dir}'

        if mods := mods_str(mod for mod in self.mods if mod.enabled):
            yield f'-mod={mods}'

        if mods := mods_str(mod for mod in self.server_mods if mod.enabled):
            yield f'-serverMod={mods}'

    @property
    def command(self) -> list[str]:
        """Returns the full command for running the server."""
        return [str(self.executable_path), *self.executable_args]

    @property
    def mods_dir(self) -> Path:
        """Returns the server's mods directory."""
        return self.base_dir / MODS_DIR

    @property
    def battleye_dir(self) -> Path:
        """Returns the profile directory."""
        return self.base_dir / 'battleye'

    @property
    def battleye_cfg_file(self) -> Path:
        """Returns the BattlEye RCon config file."""
        for path in self.battleye_dir.glob(BATTLEYE_GLOB):
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
    def enabled_mods(self) -> set[Mod]:
        """Yields enabled mods."""
        return {
            mod for mod in chain(self.mods, self.server_mods) if mod.enabled
        }

    @property
    def used_mods(self) -> Iterator[InstalledMod]:
        """Yields used mods."""
        used_ids = {mod.id for mod in chain(self.mods, self.server_mods)}

        for meta in self.installed_mods_metadata:
            if meta.publishedid in used_ids:
                yield InstalledMod(meta.publishedid, self.base_dir)

    @property
    def unused_mods(self) -> Iterator[InstalledMod]:
        """Yields unused mods."""
        used_ids = {mod.id for mod in chain(self.mods, self.server_mods)}

        for meta in self.installed_mods_metadata:
            if meta.publishedid not in used_ids:
                yield InstalledMod(meta.publishedid, self.base_dir)

    @property
    def hashes_file(self) -> Path:
        """Returns a hashes file."""
        return self.base_dir / '.hashes.json'

    @property
    def hashes(self) -> dict[str, str]:
        """Returns the server's and its mods' hashes."""
        return {
            'server': self.sha1sum,
            **{str(mod.id): mod.sha1sum for mod in self.used_mods}
        }

    @property
    def needs_restart(self) -> bool:
        """Checks whether the server needs a restart."""
        return hash_changed(self.hashes, self.load_hashes())

    @property
    def update_lockfile(self) -> LockFile:
        """Returns the path to the update lock file."""
        return LockFile(self.base_dir / '.update.lck', reason='Server update.')

    @property
    def copy_dir(self) -> Path:
        """Returns the path to the server copy dir."""
        return self.base_dir / '.update_copy'

    def chdir(self, base_dir: Path) -> Server:
        """Returns a server copy with a changed base dir."""
        return Server(
            self.name, self.app_id, base_dir, self.executable,
            self.mods, self.server_mods, self.params
        )

    def update_hashes(self) -> None:
        """Updates the hashes file."""
        with self.hashes_file.open('w', encoding='utf-8') as file:
            dump(self.hashes, file)

    def load_hashes(self) -> dict[str, str]:
        """Loads hashes for the server."""
        try:
            with self.hashes_file.open('rb') as file:
                return load(file)
        except FileNotFoundError:
            return {}

    def rcon(self, timeout: float | None = None):
        """Returns an RCon client."""
        return Client(
            (config := self.battleye_cfg).get('RConIP', '127.0.0.1'),
            config.get('RConPort', 2302),
            passwd=config['RConPassword'],
            timeout=timeout
        )

    def countdown(self, template: str, countdown: int = 120) -> None:
        """Notify users with a countdown."""
        if countdown <= 0:
            return

        with self.rcon() as rcon:
            rcon.countdown(template, countdown)

    def kick(self, player: int | str, reason: str | None = None) -> None:
        """Kicks the respective player."""
        with self.rcon(timeout=1) as rcon:
            rcon.kick(player, reason=reason)

    def kick_all(self, reason: str | None = None) -> None:
        """Kick all players."""
        with self.rcon(timeout=1) as rcon:
            for player in range(self.config.getint('maxPlayers')):
                rcon.kick(player, reason=reason)

    def shutdown(self) -> None:
        """Shutdown the server."""
        with self.rcon(timeout=1) as rcon:
            rcon.shutdown()


def load_servers_json(file: Path) -> dict[str, Any]:
    """Loads servers from a JSON file."""

    with file.open('rb') as json:
        return load(json)


def load_servers(file: Path = JSON_FILE) -> dict[str, Server]:
    """Loads servers."""

    return {
        name: Server.from_json(name, json)
        for name, json in load_servers_json(file).items()
    }
