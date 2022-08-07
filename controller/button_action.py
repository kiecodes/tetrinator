from enum import Enum


class ButtonAction(Enum):
    NOTHING = int("00000000", 2),
    RIGHT = int("10000000", 2),
    LEFT = int("01000000", 2),
    DOWN = int("00100000", 2),
    UP = int("00010000", 2),
    START = int("00001000", 2),
    SELECT = int("00000100", 2),
    B = int("00000010", 2),
    A = int("00000001", 2)
