from typing import Set

from src.event import Event


class ReadData:
    def __init__(self, events: Set[Event], errors: Set[int]):
        self.events = events
        self.errors = errors
