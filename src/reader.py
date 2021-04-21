import os
from typing import List, Dict
import yaml

from src.event import Event

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
