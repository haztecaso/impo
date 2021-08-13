from dataclasses import dataclass
from gettext import gettext as _

class InvalidSpan(Exception):
    """Exception for invalid spans"""
    pass


@dataclass(frozen=True, order=True)
class Span:
    start: int
    end: int

    def __post_init__(self):
        if self.start <= 0:
            raise InvalidSpan(_("The start value must be greater than 0"))
        if self.start > self.end:
            raise InvalidSpan(_("The end value must be greater than the start one"))

    @property
    def size(self):
        return self.end - self.start + 1

    def validate(self, n):
        if n <= 0:
            raise InvalidSpan(_("The number of pages must be greater than 0"))
        if self.end > n:
            raise InvalidSpan(_("The end value must be less or equal than the number of pages"))
        return True
