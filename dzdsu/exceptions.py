"""Common exceptions."""


__all__ = ['FailedModUpdates']


class FailedModUpdates(Exception):
    """Indicates that some mod updates failed."""

    def __init__(self, failed_updates: set[int]):
        super().__init__(failed_updates)
        self.failed_updates = failed_updates
