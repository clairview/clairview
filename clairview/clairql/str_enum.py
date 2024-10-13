from enum import Enum


class StrEnum(str, Enum):
    """
    Custom implementation of StrEnum for Python 3.10.
    This class mimics the behavior of the built-in StrEnum in Python 3.11.
    """
    def __str__(self):
        return str(self.value)