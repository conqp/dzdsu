"""Lock file implementation."""

from pathlib import Path


__all__ = ['LockFile']


class LockFile:
    """A lock file."""

    def __init__(self, file: Path):
        self.file = file

    def __getattr__(self, item):
        return getattr(self.file, item)

    def __enter__(self):
        if self.file.exists():
            raise FileExistsError()

        with self.file.open('wb') as file:
            file.write(b'locked')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.unlink()
