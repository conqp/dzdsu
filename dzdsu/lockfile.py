"""Lock file implementation."""

from os import linesep
from pathlib import Path


__all__ = ['LockFile']


class LockFile:
    """A lock file."""

    def __init__(
            self,
            file: Path,
            reason: str = 'locked',
            *,
            override: bool = False
    ):
        self.file = file
        self.reason = reason
        self.override = override

    def __getattr__(self, item):
        return getattr(self.file, item)

    def __enter__(self):
        if self.file.exists() and not self.override:
            raise FileExistsError()

        with self.file.open('w', encoding='utf-8') as file:
            file.write(self.reason)
            file.write(linesep)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.unlink()
