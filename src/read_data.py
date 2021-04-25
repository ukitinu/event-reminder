from typing import Set

from src.event import Event


class ReadData:
    def __init__(self, events: Set[Event], errors: Set[int]):
        self.__events = events
        self.__errors = errors

    @property
    def events(self):
        return self.__events

    @property
    def errors(self):
        return self.__errors
