import unittest

from moves import Stone


class TestStone(unittest.TestCase):
    def test_rotating_stone_0(self):
        sut = Stone(0)
        sut.rotate()
        self.assertEqual(sut.stone_id, 1)
        sut.rotate()
        self.assertEqual(sut.stone_id, 2)
        sut.rotate()
        self.assertEqual(sut.stone_id, 3)
        sut.rotate()
        self.assertEqual(sut.stone_id, 0)

    def test_rotating_stone_1(self):
        sut = Stone(1)
        sut.rotate()
        self.assertEqual(sut.stone_id, 2)
        sut.rotate()
        self.assertEqual(sut.stone_id, 3)
        sut.rotate()
        self.assertEqual(sut.stone_id, 0)
        sut.rotate()
        self.assertEqual(sut.stone_id, 1)

    def test_rotating_stone_2(self):
        sut = Stone(2)
        sut.rotate()
        self.assertEqual(sut.stone_id, 3)
        sut.rotate()
        self.assertEqual(sut.stone_id, 0)
        sut.rotate()
        self.assertEqual(sut.stone_id, 1)
        sut.rotate()
        self.assertEqual(sut.stone_id, 2)

    def test_rotating_stone_3(self):
        sut = Stone(3)
        sut.rotate()
        self.assertEqual(sut.stone_id, 0)
        sut.rotate()
        self.assertEqual(sut.stone_id, 1)
        sut.rotate()
        self.assertEqual(sut.stone_id, 2)
        sut.rotate()
        self.assertEqual(sut.stone_id, 3)

    def test_rotating_stone_4(self):
        sut = Stone(4)
        sut.rotate()
        self.assertEqual(sut.stone_id, 5)
        sut.rotate()
        self.assertEqual(sut.stone_id, 6)
        sut.rotate()
        self.assertEqual(sut.stone_id, 7)
        sut.rotate()
        self.assertEqual(sut.stone_id, 4)

    def test_rotating_stone_5(self):
        sut = Stone(5)
        sut.rotate()
        self.assertEqual(sut.stone_id, 6)
        sut.rotate()
        self.assertEqual(sut.stone_id, 7)
        sut.rotate()
        self.assertEqual(sut.stone_id, 4)
        sut.rotate()
        self.assertEqual(sut.stone_id, 5)

    def test_rotating_stone_6(self):
        sut = Stone(6)
        sut.rotate()
        self.assertEqual(sut.stone_id, 7)
        sut.rotate()
        self.assertEqual(sut.stone_id, 4)
        sut.rotate()
        self.assertEqual(sut.stone_id, 5)
        sut.rotate()
        self.assertEqual(sut.stone_id, 6)

    def test_rotating_stone_7(self):
        sut = Stone(7)
        sut.rotate()
        self.assertEqual(sut.stone_id, 4)
        sut.rotate()
        self.assertEqual(sut.stone_id, 5)
        sut.rotate()
        self.assertEqual(sut.stone_id, 6)
        sut.rotate()
        self.assertEqual(sut.stone_id, 7)

    def test_rotating_stone_8(self):
        sut = Stone(8)
        sut.rotate()
        self.assertEqual(sut.stone_id, 9)
        sut.rotate()
        self.assertEqual(sut.stone_id, 8)

    def test_rotating_stone_9(self):
        sut = Stone(9)
        sut.rotate()
        self.assertEqual(sut.stone_id, 8)
        sut.rotate()
        self.assertEqual(sut.stone_id, 9)

    def test_rotating_stone_10(self):
        sut = Stone(10)
        sut.rotate()
        self.assertEqual(sut.stone_id, 10)

    def test_rotating_stone_11(self):
        sut = Stone(11)
        sut.rotate()
        self.assertEqual(sut.stone_id, 12)
        sut.rotate()
        self.assertEqual(sut.stone_id, 11)

    def test_rotating_stone_12(self):
        sut = Stone(12)
        sut.rotate()
        self.assertEqual(sut.stone_id, 11)
        sut.rotate()
        self.assertEqual(sut.stone_id, 12)

    def test_rotating_stone_13(self):
        sut = Stone(13)
        sut.rotate()
        self.assertEqual(sut.stone_id, 14)
        sut.rotate()
        self.assertEqual(sut.stone_id, 15)
        sut.rotate()
        self.assertEqual(sut.stone_id, 16)
        sut.rotate()
        self.assertEqual(sut.stone_id, 13)

    def test_rotating_stone_14(self):
        sut = Stone(14)
        sut.rotate()
        self.assertEqual(sut.stone_id, 15)
        sut.rotate()
        self.assertEqual(sut.stone_id, 16)
        sut.rotate()
        self.assertEqual(sut.stone_id, 13)
        sut.rotate()
        self.assertEqual(sut.stone_id, 14)

    def test_rotating_stone_15(self):
        sut = Stone(15)
        sut.rotate()
        self.assertEqual(sut.stone_id, 16)
        sut.rotate()
        self.assertEqual(sut.stone_id, 13)
        sut.rotate()
        self.assertEqual(sut.stone_id, 14)
        sut.rotate()
        self.assertEqual(sut.stone_id, 15)

    def test_rotating_stone_16(self):
        sut = Stone(16)
        sut.rotate()
        self.assertEqual(sut.stone_id, 13)
        sut.rotate()
        self.assertEqual(sut.stone_id, 14)
        sut.rotate()
        self.assertEqual(sut.stone_id, 15)
        sut.rotate()
        self.assertEqual(sut.stone_id, 16)

    def test_rotating_stone_17(self):
        sut = Stone(17)
        sut.rotate()
        self.assertEqual(sut.stone_id, 18)
        sut.rotate()
        self.assertEqual(sut.stone_id, 17)

    def test_rotating_stone_18(self):
        sut = Stone(18)
        sut.rotate()
        self.assertEqual(sut.stone_id, 17)
        sut.rotate()
        self.assertEqual(sut.stone_id, 18)


if __name__ == '__main__':
    unittest.main()
