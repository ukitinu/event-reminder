import collections
from typing import List

from src.event import Event
import re


class CronLine:
    __DAY_REGEX = '(3[01]|[12][0-9]|[1-9])'
    __MONTH_REGEX = '(1[0-2]|[1-9])'
    __WEEKDAY_REGEX = '[0-6]'
    __RANGES = {'day': list(range(1, 32)), 'month': list(range(1, 13)), 'weekday': list(range(0, 7))}

    def __init__(self, day: str, month: str, weekday: str, event: Event):
        self.day = day
        self.month = month
        self.weekday = weekday
        self.event = event

    def __str__(self):
        return f'{self.day} {self.month} {self.weekday} {self.event}'

    def __repr__(self):
        return f"CronLine('{self.day}', '{self.month}', '{self.weekday}', {repr(self.event)})"

    def __eq__(self, other):
        if not isinstance(other, CronLine):
            return False
        days = self.__check_field_equality(other, 'day')
        months = self.__check_field_equality(other, 'month')
        weekdays = self.__check_field_equality(other, 'weekday')
        return days and months and weekdays and self.event == other.event

    def is_today(self, day: int, month: int, weekday: int) -> bool:
        is_day = day in self.__get_field_nums('day')
        is_month = month in self.__get_field_nums('month')
        is_weekday = weekday in self.__get_field_nums('weekday')
        return is_day and is_month and is_weekday

    def __get_field_nums(self, attr: str) -> List[int]:
        pieces = getattr(self, attr).split(',')
        times: List[int] = []
        for piece in pieces:
            if piece == '*':
                return self.__RANGES[attr]
            elif '-' in piece:
                start = int(piece.split('-')[0])
                end = int(piece.split('-')[1])
                times.extend(range(start, end + 1))
            elif '/' in piece:
                div = int(piece.split('/')[1])
                rem = piece.split('/')[0]
                rem = 0 if rem == '*' else (int(rem) % div)
                times.extend([i for i in self.__RANGES[attr] if i % div == rem])
            else:
                times.append(int(piece))

        return times

    def __check_field_equality(self, other, attr: str) -> bool:
        if not isinstance(other, CronLine):
            return False
        return collections.Counter(self.__get_field_nums(attr)) == collections.Counter(other.__get_field_nums(attr))

    @classmethod
    def from_string(cls, string: str):
        fields = [s.strip() for s in string.split(' ') if s.strip()]

        if len(fields) != 4:
            raise AttributeError(f'"{string}" line is not valid')

        day = fields[0]
        month = fields[1]
        weekday = fields[2]
        event = Event.from_string(fields[3])

        CronLine.__check_cron_field(day, cls.__DAY_REGEX)
        CronLine.__check_cron_field(month, cls.__MONTH_REGEX)
        CronLine.__check_cron_field(weekday, cls.__WEEKDAY_REGEX)

        return cls(day, month, weekday, event)

    @staticmethod
    def __check_cron_field(string: str, num_range: str) -> None:
        pieces = string.split(',')
        range_regex = num_range + '-' + num_range

        for piece in pieces:
            is_num = bool(re.fullmatch(num_range, piece))
            is_range = bool(re.fullmatch(range_regex, piece)) and int(piece.split('-')[0]) <= int(piece.split('-')[1])
            is_all = bool(re.fullmatch('\\*', piece))
            is_div = bool(re.fullmatch('(\\*|[1-9][0-9]|[0-9])/([1-9][0-9]|[1-9])', piece))

            if not (is_num or is_range or is_all or is_div):
                raise AttributeError(f'"{string}" cron field is not valid')
