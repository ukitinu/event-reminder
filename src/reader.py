import os
from typing import Set

from src.cronline import CronLine
from src.event import Event
from src.read_data import ReadData


def read_lines(file_path: str, day: int, month: int, weekday: int) -> ReadData:
    events: Set[Event] = set()
    errors: Set[int] = set()

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            line_num = 0
            for line in file:
                line_num += 1
                try:
                    cron = CronLine.from_string(line)
                    if cron is not None and cron.is_today(day, month, weekday):
                        events.add(cron.event)
                except AttributeError:
                    errors.add(line_num)

            return ReadData(events, errors)
    else:
        raise FileNotFoundError(f'Data file not found: {file_path}')
