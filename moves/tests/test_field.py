import unittest

from moves import Field
from moves.field import FIELD_COLS, FIELD_ROWS


class TestField(unittest.TestCase):
    def test_empty_field(self):
        sut = Field()

        for x in range(FIELD_COLS):
            for y in range(FIELD_ROWS):
                self.assertEqual(sut.get(x, y), 0)

    def test_init_with_valid_data(self):
        data = [[0]*FIELD_COLS for _ in range(FIELD_ROWS)]
        Field(data=data)

        data[10][5] = 1
        Field(data=data)

    def test_eq(self):
        self.assertEqual(Field(), Field())

    def test_set(self):
        sut = Field()
        sut.set(0, 0, 1)
        self.assertEqual(sut.get(0, 0), 1)


if __name__ == '__main__':
    unittest.main()
