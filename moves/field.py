from typing import List

FIELD_COLS = 10
FIELD_ROWS = 20


class Field:
    """
    Represents a field of 10x20 fields of 0s and 1s
    Field (0, 0) is in the top left corner
    """

    def __init__(self, data=None):
        if data is not None:
            self.set_data(data)
        else:
            self._data = [([0] * FIELD_COLS) for _ in range(FIELD_ROWS)]

    def set(self, x, y, value):
        self._data[y][x] = value

    def get(self, x, y) -> int:
        return self._data[y][x]

    def get_row(self, y) -> List[int]:
        return self._data[y]

    def set_data(self, data):
        self._data = data

    @staticmethod
    def contains(x, y) -> bool:
        return 0 <= x < FIELD_COLS and 0 <= y < FIELD_ROWS

    def __eq__(self, other) -> bool:
        return self._data == other._data

    def __repr__(self) -> str:
        return "\n"+"\n".join(map(lambda row: ",".join(map(str, row)), self._data))+"\n"

    def print(self):
        print("\n"+"\n".join(map(lambda row: "".join(map(lambda e: "▓▓" if e > 0 else "░░", row)), self._data))+"\n")

