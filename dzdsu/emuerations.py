"""Common enumerations."""

from enum import Enum


__all__ = ['ServerType']


class ServerType(Enum):
    """Available server versions."""

    VANILLA = 223350
    EXP = 1042420

    def __int__(self):
        return self.value
