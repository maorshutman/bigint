import mpint


def new_test():
    x = mpint.MPInt([1, 1, 0], bits=16)
    assert x.used == 3

    n = 456737
    x = mpint.MPInt(n, bits=32)
    assert x.used == 19

    y = mpint.MPInt(int(-1), bits=16)
    assert y.sign == mpint._MP_NEG

    z = mpint.MPInt(int(0), bits=16)
    assert z.sign == mpint._MP_ZPOS

    w = mpint.MPInt([0, 0, 0, 1, 1, 0, 1, 1, 1], bits=16)
    assert (w.used == 6) and (w.alloc == 16)


def mp_grow_test():
    x = mpint.MPInt([1, 1, 0], bits=16)
    x.mp_grow(31)
    assert x.shape[1] == 48


def mp_clamp_test():
    x = mpint.MPInt([1, 1, 0], bits=16)
    x.mp_clamp()
    assert x.used == 3

    x = mpint.MPInt([0, 0, 0, 1, 0, 0, 1, 1, 0], bits=16)
    x.mp_clamp()
    assert x.used == 6


def mp_copy_test():
    x = mpint.MPInt([1, 1, 0], bits=16)
    w = mpint.MPInt([0, 1, 1, 0, 1], bits=16)
    w.mp_copy(x)
    assert w.used == 3

    n = 456737  # 19 used bits, 0b1101111100000100001
    x = mpint.MPInt(n, bits=32)
    w = mpint.MPInt([0, 1, 1, 0, 1], bits=16)
    w.mp_copy(x)
    assert (w.used == 19) and (w.alloc == 32)


def mp_zero_test():
    c = mpint.MPInt(int(-234), bits=16)
    c.mp_zero()
    assert (c.used == 0) and (c.alloc == 16) and (c.sign == mpint._MP_ZPOS)


def mp_abs_test():
    y = mpint.MPInt(int(-1), bits=16)
    y_abs = y.mp_abs()
    assert y_abs.sign == mpint._MP_ZPOS


def mp_neg_test():
    y = mpint.MPInt(int(-1), bits=16)
    y_abs = y.mp_neg()
    assert y_abs.sign == mpint._MP_ZPOS

    y = mpint.MPInt(int(1), bits=16)
    y_abs = y.mp_neg()
    assert y_abs.sign == mpint._MP_NEG


def run():
    print("Running tests.")

    new_test()
    mp_grow_test()
    mp_clamp_test()
    mp_copy_test()
    mp_zero_test()
    mp_abs_test()
    mp_neg_test()

    print("All tests passed.")
