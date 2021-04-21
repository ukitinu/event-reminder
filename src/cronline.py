from src.event import Event
import re


class CronLine:
    __CRON_DAY_NUM = '(3[01]|[12][0-9]|[1-9])'
    __CRON_MONTH_NUM = '(1[0-2]|[1-9])'
    __CRON_WEEKDAY_NUM = '[0-6]'

    def __init__(self, day: str, month: str, weekday: str, event: Event):
        self.day = day
        self.month = month
        self.weekday = weekday
        self.event = event

    def __str__(self):
        return f'{self.day} {self.month} {self.weekday} {self.event}'

    def __repr__(self):
        return f'CronLine({self.day}, {self.month}, {self.weekday}, {repr(self.event)})'

    def __eq__(self, other):
        if not isinstance(other, CronLine):
            return False
        is_weekday_equal = (self.weekday % 7) == (other.weekday % 7)
        return self.day == other.day and self.month == other.month and is_weekday_equal and self.event == other.event

    def is_today(self, day: int, month: int, weekday: int) -> bool:
        is_day = self.is_time('day', day)
        is_month = self.is_time('month', month)
        is_weekday = self.is_time('weekday', weekday)
        return is_day and is_month and is_weekday

    def is_time(self, attr: str, num: int) -> bool:
        cron_str = getattr(self, attr)
        pieces = cron_str.split(',')
        result = False
        for piece in pieces:
            if piece == '*':
                return True
            elif '-' in piece:
                result |= CronLine.__is_in_range(piece, num)
            elif '/' in piece:
                result |= CronLine.__is_remainder(piece, num)
            else:
                result |= num == int(piece)
        return result

    @staticmethod
    def __is_in_range(piece: str, num: int) -> bool:
        start = int(piece.split('-')[0])
        end = int(piece.split('-')[1])
        return start <= num <= end

    @staticmethod
    def __is_remainder(piece: str, num: int) -> bool:
        rem = piece.split('/')[0]
        rem = 0 if rem == '*' else int(rem)
        div = int(piece.split('/')[1])
        return num % div == rem

    @classmethod
    def from_string(cls, string: str):
        fields = [s.strip() for s in string.split(' ') if s.strip()]

        if len(fields) != 4:
            raise AttributeError(f'"{string}" line is not valid')

        day = fields[0]
        month = fields[1]
        weekday = fields[2]
        event = Event.from_string(fields[3])

        CronLine.__check_cron_field(day, cls.__CRON_DAY_NUM)
        CronLine.__check_cron_field(month, cls.__CRON_MONTH_NUM)
        CronLine.__check_cron_field(weekday, cls.__CRON_WEEKDAY_NUM)

        return cls(day, month, weekday, event)

    @staticmethod
    def __check_cron_field(string: str, num_range: str) -> None:
        pieces = string.split(',')

        for piece in pieces:
            is_num = bool(re.fullmatch(num_range, piece))
            is_range = bool(re.fullmatch(num_range + '-' + num_range, piece))
            is_all = bool(re.fullmatch('\\*', piece))
            is_div = bool(re.fullmatch('(\\*|[1-9][0-9]|[0-9])/([1-9][0-9]|[1-9])', piece))

            if not (is_num or is_range or is_all or is_div):
                raise AttributeError(f'"{string}" cron field is not valid')
