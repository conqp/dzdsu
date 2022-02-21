"""Mission management."""

from pathlib import Path
from tarfile import TarFile
from typing import Iterator


__all__ = ['Mission']


class Mission:
    """Represents a mission."""

    def __init__(self, path: Path):
        self.path = path

    @property
    def files(self) -> Iterator[Path]:
        """Yields top-level files."""
        return self.path.iterdir()

    def backup(self, archive: Path):
        """Creates a backup of the mission."""
        with TarFile.open(archive, mode='w:gz') as tarfile:
            for file in self.files:
                tarfile.add(file)
