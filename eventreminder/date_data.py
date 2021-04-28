from typing import Set

from eventreminder.event import Event


class DateData:
    """
    Utility data-holder class to return results and errors
    """

    def __init__(self, events: Set[Event], errors: Set[int]):
        self.events = events
        self.errors = errors

    def __str__(self) -> str:
        return f"DateData: {len(self.events)} events, {len(self.errors)} errors"

    def __repr__(self) -> str:
        return f"DateData({repr(self.events)}, {repr(self.errors)})"
