from eventreminder.crontime import CronTime
from eventreminder.event import Event


class CronLine:
    __COMMENT = '#'

    def __init__(self, cron: CronTime, event: Event):
        self.cron = cron
        self.event = event

    def __str__(self):
        return f'{self.cron} {self.event}'

    def __repr__(self):
        return f'CronLine({self.cron}, {self.event})'

    def __eq__(self, other):
        if not isinstance(other, CronLine):
            return False
        return self.cron == other.cron and self.event == other.event

    def is_today(self, day: int, month: int, weekday: int) -> bool:
        """`weekday` assumes ISO 8601 (i.e. 1 is Monday, 2 is Tuesday, ..., 7 is Sunday)."""
        return self.cron.is_time(day, month, weekday)

    def to_text(self) -> str:
        return self.event.to_text()

    @classmethod
    def from_string(cls, string: str):
        if cls.__COMMENT in string:
            ignore_from = string.index(cls.__COMMENT)
            string = string[:ignore_from]

        string = ' '.join(string.split())
        if string == '':
            return None

        fields = [s.strip() for s in string.split(sep=' ', maxsplit=3) if s.strip()]

        if len(fields) != 4:
            raise AttributeError(f'"{string}" line not valid')

        cron = CronTime.from_string(f'{fields[0]} {fields[1]} {fields[2]}')
        event = Event.from_string(fields[3])

        return cls(cron, event)
