class Event:
    __STR_FORMAT = 'TITLE; DESCRIPTION[; MORE]'

    def __init__(self, title: str, desc: str, more: str = ''):
        self.title = title
        self.desc = desc
        self.more = more

    def __str__(self):
        return f'{self.title}; {self.desc}; {self.more}' if self.more else f'{self.title}; {self.desc}'

    def __repr__(self):
        return f"Event('{self.title}', '{self.desc}', '{self.more}')"

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.title == other.title and self.desc == other.desc and self.more == other.more

    def to_text(self) -> str:
        main = f'{self.title}:\n\t{self.desc}'
        return f'{main}\n\t{self.more}' if self.more else main

    @classmethod
    def from_string(cls, string: str):
        string = ' '.join(string.split())
        fields = [s.strip() for s in string.split(';') if s.strip()]

        if len(fields) != 2 and len(fields) != 3:
            raise AttributeError(f'"{string}" format is not {cls.__STR_FORMAT}')

        title = fields[0]
        desc = fields[1]
        more = fields[2] if fields[2:] else ''
        return cls(title, desc, more)
