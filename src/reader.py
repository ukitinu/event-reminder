import os
from typing import List, Dict, Set
import yaml

from src.cronline import CronLine
from src.event import Event
from src.read_data import ReadData

MONTH_NAMES: Dict[int, str] = {
    1: 'gennaio',
    2: 'febbraio',
    3: 'marzo',
    4: 'aprile',
    5: 'maggio',
    6: 'giugno',
    7: 'luglio',
    8: 'agosto',
    9: 'settembre',
    10: 'ottobre',
    11: 'novembre',
    12: 'dicembre',
}


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


def read_data(file_path: str, month: str, day: int) -> List[Event]:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return get_day_data(data, month, day)
    else:
        raise FileNotFoundError(f'Data file not found: {file_path}')


def get_day_data(data, month, day) -> List[Event]:
    try:
        return [Event.from_string(e) for e in data[month][day]]
    except KeyError:
        return []
    except AttributeError as ae:
        raise ae


def get_month(num: int) -> str:
    return MONTH_NAMES.get(num, 'invalid month')
