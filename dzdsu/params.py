"""Server start parameters."""

from typing import NamedTuple, Iterator, Optional

from dzdsu.constants import CONFIG_FILE


__all__ = ['ServerParams']


class ServerParams(NamedTuple):
    """Available server start parameters."""

    config: str = CONFIG_FILE
    do_logs: bool = True
    admin_log: bool = True
    net_log: bool = True
    src_allow_file_write: bool = True
    no_file_patching: bool = True
    freeze_check: bool = True
    port: Optional[int] = None
    profiles: Optional[str] = None
    cpu_count: Optional[int] = None

    @classmethod
    def from_json(cls, json: dict):
        """Creates a ServerParams instance from a JSON-ish dict."""
        return cls(
            json.get('config', CONFIG_FILE),
            json.get('doLogs', True),
            json.get('adminLog', True),
            json.get('netLog', True),
            json.get('srcAllowFileWrite', True),
            json.get('noFilePatching', True),
            json.get('freezeCheck', True),
            json.get('port'),
            json.get('profiles'),
            json.get('cpuCount')
        )

    @property
    def executable_args(self) -> Iterator[str]:
        """Yields arguments for the server executable."""
        yield f'-config={self.config}'

        if self.do_logs:
            yield '-doLogs'

        if self.admin_log:
            yield '-adminLog'

        if self.net_log:
            yield '-netLog'

        if self.src_allow_file_write:
            yield '-srcAllowFileWrite'

        if self.no_file_patching:
            yield '-noFilePatching'

        if self.freeze_check:
            yield '-freezeCheck'

        if self.port is not None:
            yield f'-port={self.port}'

        if self.profiles is not None:
            yield f'-profiles={self.profiles}'

        if self.cpu_count is not None:
            yield f'-cpuCount={self.cpu_count}'
