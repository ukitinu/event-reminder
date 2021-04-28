import os
from typing import Set

from eventreminder.cronline import CronLine
from eventreminder.event import Event
from eventreminder.date_data import DateData


def read_lines(file_path: str, day: int, month: int, weekday: int) -> DateData:
    events: Set[Event] = set()
    errors: Set[int] = set()

    if os.path.exists(file_path):
        if os.path.islink(file_path):
            file_path = os.readlink(file_path)
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

            return DateData(events, errors)
    else:
        raise FileNotFoundError(f'Data file not found: {file_path}')
