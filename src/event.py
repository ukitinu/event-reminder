class Event:
    __STR_FORMAT = 'WHO; WHAT[; OTHER]'

    def __init__(self, who: str, what: str, other: str = ''):
        self.who = who
        self.what = what
        self.other = other

    def __str__(self):
        return f'{self.who}; {self.what}; {self.other}' if self.other else f'{self.who}; {self.what}'

    def __repr__(self):
        return f"Event('{self.who}', '{self.what}', '{self.other}')"

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.who == other.who and self.what == other.what and self.other == other.other

    def to_text(self) -> str:
        main = f'{self.who}:\n\t{self.what}'
        return f'{main}\n\t{self.other}' if self.other else main

    @classmethod
    def from_string(cls, string: str):
        string = ' '.join(string.split())
        fields = [s.strip() for s in string.split(';') if s.strip()]

        if len(fields) != 2 and len(fields) != 3:
            raise AttributeError(f'"{string}" format is not {cls.__STR_FORMAT}')

        who = fields[0]
        what = fields[1]
        other = fields[2] if fields[2:] else ''
        return cls(who, what, other)
