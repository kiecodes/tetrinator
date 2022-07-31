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

    def test_init_with_to_short_field(self):
        with self.assertRaises(AssertionError):
            Field(data=[[0]*FIELD_COLS for _ in range(FIELD_ROWS-1)])

    def test_init_with_to_narrow_field(self):
        with self.assertRaises(AssertionError):
            Field(data=[[0]*(FIELD_COLS-1) for _ in range(FIELD_ROWS)])

    def test_init_with_to_skewed_field(self):
        data = [[0] * FIELD_COLS for _ in range(FIELD_ROWS)]
        data[5] = [0] * 4
        with self.assertRaises(AssertionError):
            Field(data=data)

    def test_init_with_invalid_value_in_field(self):
        data = [[0] * FIELD_COLS for _ in range(FIELD_ROWS)]
        data[5][3] = 2
        with self.assertRaises(AssertionError):
            Field(data=data)

    def test_init_with_invalid_value_type_in_field(self):
        data = [[0] * FIELD_COLS for _ in range(FIELD_ROWS)]
        data[5][3] = "2"
        with self.assertRaises(AssertionError):
            Field(data=data)

    def test_eq(self):
        self.assertEqual(Field(), Field())

    def test_set(self):
        sut = Field()
        sut.set(0, 0, 1)
        self.assertEqual(sut.get(0, 0), 1)


if __name__ == '__main__':
    unittest.main()
