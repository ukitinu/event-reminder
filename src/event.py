class Event:
    __STR_FORMAT = 'WHO; WHAT[; OTHER]'

    def __init__(self, who: str, what: str, other: str = ''):
        self.who = who
        self.what = what
        self.other = other

    def __str__(self):
        main = f'{self.who}:\n\t{self.what}'
        return f'{main}\n\t{self.other}' if self.other else main

    def __repr__(self):
        return f'Event({self.who}, {self.what}, {self.other})'

    @classmethod
    def from_string(cls, string: str):
        fields = [s.strip() for s in string.split(';') if s.strip()]
        if len(fields) != 2 and len(fields) != 3:
            raise AttributeError(f'{string} format is not {cls.__STR_FORMAT}')
        who = fields[0].strip()
        what = fields[1].strip()
        other = fields[2].strip() if fields[2:] else ''
        return cls(who, what, other)
