import unittest
import mpint


# TODO: How to use constants from mpint correctly ?

class TestMPInt(unittest.TestCase):
    def test_new(self):
        x = mpint.MPInt([1, 1, 0], bits=mpint._MP_PREC)
        self.assertEqual(x.used, 3)

        n = 456737
        x = mpint.MPInt(n, bits=2*mpint._MP_PREC)
        self.assertEqual(x.used, 19)

        y = mpint.MPInt(int(-1), bits=mpint._MP_PREC)
        self.assertEqual(y.sign, mpint._MP_NEG)

        z = mpint.MPInt(int(0), bits=mpint._MP_PREC)
        self.assertEqual(z.sign, mpint._MP_ZPOS)

        w = mpint.MPInt([0, 0, 0, 1, 1, 0, 1, 1, 1], bits=mpint._MP_PREC)
        self.assertEqual(w.used, 6)
        self.assertEqual(w.alloc, mpint._MP_PREC)

    def test_mp_grow(self):
        x = mpint.MPInt([1, 1, 0], bits=mpint._MP_PREC)
        x.mp_grow(31)
        self.assertEqual(x.shape[1], 32)

        x = mpint.MPInt([1, 1, 0], bits=mpint._MP_PREC)
        x.mp_grow(33)
        self.assertEqual(x.shape[1], 96)

    def test_mp_clamp(self):
        x = mpint.MPInt([1, 1, 0], bits=mpint._MP_PREC)
        x.mp_clamp()
        self.assertEqual(x.used, 3)

        x = mpint.MPInt([0, 0, 0, 1, 0, 0, 1, 1, 0], bits=mpint._MP_PREC)
        x.mp_clamp()
        self.assertEqual(x.used, 6)

    def test_mp_copy(self):
        x = mpint.MPInt([1, 1, 0], bits=mpint._MP_PREC)
        w = mpint.MPInt([0, 1, 1, 0, 1], bits=mpint._MP_PREC)
        w.mp_copy(x)
        self.assertEqual(w.used, 3)

        n = 456737  # 19 used bits, 0b1101111100000100001
        x = mpint.MPInt(n, bits=2*mpint._MP_PREC)
        w = mpint.MPInt([0, 1, 1, 0, 1], bits=mpint._MP_PREC)
        w.mp_copy(x)
        self.assertEqual(w.used, 19)
        self.assertEqual(w.alloc, 2*mpint._MP_PREC)

    def test_mp_zero(self):
        c = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        c.mp_zero()
        self.assertEqual(c.used, 0)
        self.assertEqual(c.alloc, mpint._MP_PREC)
        self.assertEqual(c.sign, mpint._MP_ZPOS)

    def test_mp_abs(self):
        y = mpint.MPInt(int(-1), bits=mpint._MP_PREC)
        y_abs = y.mp_abs()
        self.assertEqual(y_abs.sign, mpint._MP_ZPOS)

    def test_mp_neg(self):
        y = mpint.MPInt(int(-1), bits=mpint._MP_PREC)
        y_abs = y.mp_neg()
        self.assertEqual(y_abs.sign, mpint._MP_ZPOS)

        y = mpint.MPInt(int(1), bits=mpint._MP_PREC)
        y_abs = y.mp_neg()
        self.assertEqual(y_abs.sign, mpint._MP_NEG)

        y = mpint.MPInt(0, bits=mpint._MP_PREC)
        y_abs = y.mp_neg()
        self.assertEqual(y_abs.sign, mpint._MP_ZPOS)

    def test_mp_cmp_mag(self):
        x = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp_mag(x, y), mpint._MP_EQ)

        x = mpint.MPInt(int(-15), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp_mag(x, y), mpint._MP_LT)

        x = mpint.MPInt(int(234), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp_mag(x, y), mpint._MP_EQ)

        x = mpint.MPInt(0, bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-0), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp_mag(x, y), mpint._MP_EQ)

        x = mpint.MPInt(456737, bits=2*mpint._MP_PREC)
        y = mpint.MPInt(456736, bits=2*mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp_mag(x, y), mpint._MP_GT)

    def test_mp_cmp(self):
        x = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp(x, y), mpint._MP_EQ)

        x = mpint.MPInt(int(-15), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp(x, y), mpint._MP_GT)

        x = mpint.MPInt(int(234), bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-234), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp(x, y), mpint._MP_GT)

        x = mpint.MPInt(0, bits=mpint._MP_PREC)
        y = mpint.MPInt(int(-0), bits=mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp(x, y), mpint._MP_EQ)

        x = mpint.MPInt(456737, bits=2*mpint._MP_PREC)
        y = mpint.MPInt(456736, bits=2*mpint._MP_PREC)
        self.assertEqual(mpint.MPInt.mp_cmp(x, y), mpint._MP_GT)


if __name__ == '__main__':
    unittest.main()
