from typing import List

STONE_SIZE = 4


class Stone:
    def __init__(self, stone_id: int):
        self._stone_id = stone_id
        self._data = self._stone_by_id(stone_id)

    def get(self, x, y):
        assert 0 <= x < STONE_SIZE and 0 <= y < STONE_SIZE
        return self._data[y*STONE_SIZE+x]

    def change(self, stone_id):
        self._stone_id = stone_id
        self._data = self._stone_by_id(stone_id)

    @property
    def stone_id(self):
        return self._stone_id

    @staticmethod
    def _stone_by_id(stone_id: int) -> List[int]:
        if stone_id == 0:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 1, 1, 1]
        elif stone_id == 1:
            return [0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 1,
                    0, 0, 1, 0]
        elif stone_id == 2:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 1, 1,
                    0, 0, 1, 0]
        elif stone_id == 3:
            return [0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 1, 1, 0,
                    0, 0, 1, 0]
        elif stone_id == 4:
            return [0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 0,
                    0, 1, 1, 0]
        elif stone_id == 5:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 1, 1, 1]
        elif stone_id == 6:
            return [0, 0, 0, 0,
                    0, 0, 1, 1,
                    0, 0, 1, 0,
                    0, 0, 1, 0]
        elif stone_id == 7:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 1, 1,
                    0, 0, 0, 1]
        elif stone_id == 8:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 1, 0,
                    0, 0, 1, 1]
        elif stone_id == 9:
            return [0, 0, 0, 0,
                    0, 0, 0, 1,
                    0, 0, 1, 1,
                    0, 0, 1, 0]
        elif stone_id == 10:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 1, 0,
                    0, 1, 1, 0]
        elif stone_id == 11:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 1, 1,
                    0, 1, 1, 0]
        elif stone_id == 12:
            return [0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 1,
                    0, 0, 0, 1]
        elif stone_id == 13:
            return [0, 0, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 1]
        elif stone_id == 14:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 1, 1, 1,
                    0, 1, 0, 0]
        elif stone_id == 15:
            return [0, 0, 0, 0,
                    0, 1, 1, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 0]
        elif stone_id == 16:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 1,
                    0, 1, 1, 1]
        elif stone_id == 17:
            return [0, 0, 1, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 0,
                    0, 0, 1, 0]
        elif stone_id == 18:
            return [0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    1, 1, 1, 1]
        else:
            raise ValueError(f"unknown stone id {stone_id}")

    def num_rotations(self) -> int:
        if 0 <= self._stone_id <= 3:
            return 4
        elif 4 <= self._stone_id <= 7:
            return 4
        elif 8 <= self._stone_id <= 9:
            return 2
        elif self._stone_id == 10:
            return 1
        elif 11 <= self._stone_id <= 12:
            return 2
        elif 13 <= self._stone_id <= 16:
            return 4
        elif 17 <= self._stone_id <= 18:
            return 2
        else:
            raise ValueError(f"unknown stone id {self._stone_id}")

    def get_base_stone_id(self) -> int:
        if 0 <= self._stone_id <= 3:
            return 0
        elif 4 <= self._stone_id <= 7:
            return 4
        elif 8 <= self._stone_id <= 9:
            return 8
        elif self._stone_id == 10:
            return 10
        elif 11 <= self._stone_id <= 12:
            return 11
        elif 13 <= self._stone_id <= 16:
            return 13
        elif 17 <= self._stone_id <= 18:
            return 17
        else:
            raise ValueError(f"unknown stone id {self._stone_id}")

    def get_height(self) -> int:
        if self._stone_id == 0:
            return 2
        elif self._stone_id == 1:
            return 3
        elif self._stone_id == 2:
            return 2
        elif self._stone_id == 3:
            return 3
        elif self._stone_id == 4:
            return 3
        elif self._stone_id == 5:
            return 2
        elif self._stone_id == 6:
            return 3
        elif self._stone_id == 7:
            return 2
        elif self._stone_id == 8:
            return 2
        elif self._stone_id == 9:
            return 3
        elif self._stone_id == 10:
            return 2
        elif self._stone_id == 11:
            return 2
        elif self._stone_id == 12:
            return 3
        elif self._stone_id == 13:
            return 3
        elif self._stone_id == 14:
            return 2
        elif self._stone_id == 15:
            return 3
        elif self._stone_id == 16:
            return 2
        elif self._stone_id == 17:
            return 4
        elif self._stone_id == 18:
            return 1
        else:
            raise ValueError(f"unknown stone id {self._stone_id}")

    def rotate(self):
        base_stone_id = self.get_base_stone_id()
        self.change(base_stone_id + (self._stone_id - base_stone_id + 1) % self.num_rotations())
