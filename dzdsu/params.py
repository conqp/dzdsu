"""Server start parameters."""

from multiprocessing import cpu_count
from typing import NamedTuple, Iterator, Optional

from dzdsu.constants import CONFIG_FILE


__all__ = ['ServerParams']


class ServerParams(NamedTuple):
    """Available server start parameters."""

    config_file: str = CONFIG_FILE
    do_logs: bool = True
    admin_log: bool = True
    net_log: bool = True
    src_allow_file_write: bool = True
    no_file_patching: bool = True
    freeze_check: bool = True
    instance_id: Optional[int] = None
    port: Optional[int] = None
    profiles_dir: Optional[str] = None
    cpus: Optional[int] = None

    @classmethod
    def from_json(cls, json: dict):
        """Creates a ServerParams instance from a JSON-ish dict."""
        return cls(
            json.get('config_file', CONFIG_FILE),
            json.get('do_logs', True),
            json.get('admin_log', True),
            json.get('net_log', True),
            json.get('src_allow_file_write', True),
            json.get('no_file_patching', True),
            json.get('freeze_check', True),
            json.get('instance_id'),
            json.get('port'),
            json.get('profiles_dir'),
            json.get('cpus', cpu_count())
        )

    def get_binary_args(self) -> Iterator[str]:
        """Yields arguments for the server binary."""
        yield f'-config={self.config_file}'

        if self.do_logs:
            yield '-dologs'

        if self.admin_log:
            yield '-adminlog'

        if self.net_log:
            yield '-netlog'

        if self.src_allow_file_write:
            yield '-srcAllowFileWrite'

        if self.no_file_patching:
            yield '-noFilePatching'

        if self.freeze_check:
            yield '-freezecheck'

        if self.instance_id is not None:
            yield f'-instanceId={self.instance_id}'

        if self.port is not None:
            yield f'-port={self.port}'

        if self.profiles_dir is not None:
            yield f'-profiles={self.profiles_dir}'

        if self.cpus is not None:
            yield f'-cpuCount={self.cpus}'
