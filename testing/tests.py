import unittest
import mpint


class TestMPInt(unittest.TestCase):
    def test_new(self):
        x = mpint.MPInt([1, 1, 0], bits=16)
        self.assertEqual(x.used, 3)

        n = 456737
        x = mpint.MPInt(n, bits=32)
        self.assertEqual(x.used, 19)

        y = mpint.MPInt(int(-1), bits=16)
        self.assertEqual(y.sign, mpint._MP_NEG)

        z = mpint.MPInt(int(0), bits=16)
        self.assertEqual(z.sign, mpint._MP_ZPOS)

        w = mpint.MPInt([0, 0, 0, 1, 1, 0, 1, 1, 1], bits=16)
        self.assertEqual(w.used, 6)
        self.assertEqual(w.alloc, 16)

    def test_mp_grow(self):
        x = mpint.MPInt([1, 1, 0], bits=16)
        x.mp_grow(31)
        self.assertEqual(x.shape[1], 48)

    def test_mp_clamp(self):
        x = mpint.MPInt([1, 1, 0], bits=16)
        x.mp_clamp()
        self.assertEqual(x.used, 3)

        x = mpint.MPInt([0, 0, 0, 1, 0, 0, 1, 1, 0], bits=16)
        x.mp_clamp()
        self.assertEqual(x.used, 6)

    def test_mp_copy(self):
        x = mpint.MPInt([1, 1, 0], bits=16)
        w = mpint.MPInt([0, 1, 1, 0, 1], bits=16)
        w.mp_copy(x)
        self.assertEqual(w.used, 3)

        n = 456737  # 19 used bits, 0b1101111100000100001
        x = mpint.MPInt(n, bits=32)
        w = mpint.MPInt([0, 1, 1, 0, 1], bits=16)
        w.mp_copy(x)
        self.assertEqual(w.used, 19)
        self.assertEqual(w.alloc, 32)

    def test_mp_zero(self):
        c = mpint.MPInt(int(-234), bits=16)
        c.mp_zero()
        self.assertEqual(c.used, 0)
        self.assertEqual(c.alloc, 16)
        self.assertEqual(c.sign, mpint._MP_ZPOS)

    def test_mp_abs(self):
        y = mpint.MPInt(int(-1), bits=16)
        y_abs = y.mp_abs()
        self.assertEqual(y_abs.sign, mpint._MP_ZPOS)

    def test_mp_neg(self):
        y = mpint.MPInt(int(-1), bits=16)
        y_abs = y.mp_neg()
        self.assertEqual(y_abs.sign, mpint._MP_ZPOS)

        y = mpint.MPInt(int(1), bits=16)
        y_abs = y.mp_neg()
        self.assertEqual(y_abs.sign, mpint._MP_NEG)


if __name__ == '__main__':
    unittest.main()
