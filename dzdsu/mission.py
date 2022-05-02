"""Mission management."""

from pathlib import Path
from shutil import rmtree
from tarfile import TarFile


__all__ = ['Mission']


class Mission:
    """Represents a mission."""

    def __init__(self, path: Path):
        if not path.is_absolute():
            raise ValueError('Refusing to create mission from relative path.')

        if not path.is_dir():
            raise FileNotFoundError('No such mission:', path)

        self.path = path

    @property
    def name(self) -> str:
        """Returns the mission name."""
        return self.path.name

    @property
    def storage_1(self) -> Path:
        """Returns the path to the storage_1 folder."""
        return self.path / 'storage_1'

    def backup(self, archive: Path) -> None:
        """Creates a backup of the mission."""
        with TarFile.open(archive, mode='w:gz') as tarfile:
            for file_or_dir in self.path.iterdir():
                tarfile.add(file_or_dir)

    def wipe(self) -> None:
        """Wipes the mission data."""
        for file_or_dir in self.storage_1.iterdir():
            if file_or_dir.is_dir():
                rmtree(file_or_dir)
            else:
                file_or_dir.unlink()
