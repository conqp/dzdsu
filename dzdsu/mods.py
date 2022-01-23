"""Modifications from the Steam workshop."""

from typing import NamedTuple


__all__ = ['Mod']


class Mod(NamedTuple):
    """Represents a mod."""

    id: int
    name: str
    disabled: bool = False

    @classmethod
    def from_json(cls, json: dict):
        """Creates an instance of Mod from a JSON-ish dict."""
        return cls(json['id'], json['name'], json.get('disabled', False))
