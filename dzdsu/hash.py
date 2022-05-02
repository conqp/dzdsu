"""Watchdog to detect server and mod updates."""


__all__ = ['hash_changed']


def hash_changed(old: dict[str, str], new: dict[str, str]) -> bool:
    """Returns True iff the hashes are not equal."""

    for key, value in old.items():
        if (new_value := new.get(key)) is not None and new_value != value:
            return True

    return any(key not in old for key in new)
