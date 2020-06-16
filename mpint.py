import numpy as np
import torch

# TODO: Consider arbitrary base ?


_MP_PREC = 16
_MP_ZPOS = 1
_MP_NEG = 0


class MPInt(torch.Tensor):
    """Multiple-Precision Integer."""

    def __new__(cls, x, bits, sign=_MP_ZPOS, *args, **kwargs):
        # Input validity check.
        assert bits % _MP_PREC == 0, "Number of bits should be divisible by {}.".format(_MP_PREC)

        # Convert input to binary list and pad to multiple of _MP_PREC.
        if type(x) == int:
            x = cls._py_int_to_tensor(x, bits)
        elif type(x) == list:
            x = cls._lsb_order(x)
            x = cls._zero_pad(x, bits)
        assert bits == len(x)

        # Tensor size will be 1 x bits.
        return super().__new__(cls, [x], *args, **kwargs)

    def __init__(self, x, bits, sign=_MP_ZPOS):
        # Allocated number of bits.
        self.alloc = bits

        # User can give list and sign (1/positive by default)
        # or python int with sign
        # Sign bit.

        # With a list the user has to specify the sign. The sign is _MP_ZPOS.
        self.sign = sign
        if type(x) == int:
            self.sign = self._sign(x)

        if type(x) == list:
            self.used = self._used_in_list(x[::-1])
        elif type(x) == int:
            self.used = self._used_in_list(self._py_int_to_tensor(x, self.alloc))

    @staticmethod
    def _py_int_to_tensor(x, bits):
        """convert an arbitrary precision python int to a binary list in LSB
           order.
        """
        bin = np.binary_repr(x)
        bin_out = []
        for c in bin:
            if c in ['0', '1']:
                bin_out.append(int(c))
        bin_out.reverse()  # lsb ordering

        if bits <= len(bin_out):
            raise Exception("Not enough bits for given integer.")

        # Pad with zeros.
        bin_out = bin_out + [0] * (bits - len(bin_out))
        assert len(bin_out) == bits

        return bin_out

    @staticmethod
    def _sign(x):
        if x >= 0:
            return _MP_ZPOS
        else:
            return _MP_NEG

    @staticmethod
    def _used_in_list(x):
        """Works with LSB ordering."""
        assert type(x) == list
        num_bits = len(x)
        i = num_bits
        while (i != 0) and (x[i - 1] != 1):
            i -= 1
        return i

    # @staticmethod
    # def _used_in_py_int(x):
    #     """x is a python int."""
    #     used = 0
    #     while x != 0:
    #         used += 1
    #         x = x // 2
    #     return used

    @staticmethod
    def _zero_pad(x, alloc):
        if alloc <= len(x):
            # TODO: Print for the use how many bits are needed ?
            raise Exception("Not enough bits for given integer.")
        bin_out = x + [0] * (alloc - len(x))
        assert len(bin_out) == alloc
        return bin_out

    @staticmethod
    def _lsb_order(x):
        return x[::-1]

    # Maintenance algorithms.
    def mp_grow(self, b):
        """Extend binary vector to accommodate b digits.
           In place operation.
        """
        if b <= self.alloc:
            return

        prev_alloc = self.alloc
        self.alloc = b + 2 * _MP_PREC - b % _MP_PREC

        # TODO: This is really strange. The data inside Tensor is a Tensor ?
        pad_size = self.alloc - prev_alloc
        self.data = torch.cat([self.data, torch.zeros([1, pad_size])], dim=1)
        assert self.data.shape[1] == self.alloc

    def mp_clamp(self):
        """Remove excess zeros."""
        while self.used > 0 and self.data[0, self.used - 1] == 0:
            self.used -= 1
        if self.used == 0:
            self.sign = _MP_ZPOS

    def mp_copy(self, x):
        """Copy x."""
        self.alloc = x.alloc
        self.used = x.used
        self.sign = x.sign
        self.data = x.data

    def mp_init_copy(self):
        """Create a new copy of self."""
        cp = MPInt(0, bits=self.alloc)
        cp.mp_copy(self)
        return cp

    def mp_zero(self):
        """Zero the content."""
        self.sign = _MP_ZPOS
        self.data[0, :self.used] = 0
        self.used = 0

    def mp_abs(self):
        """Return a copy of the abs."""
        cp = self.mp_init_copy()
        cp.sign = _MP_ZPOS
        return cp

    def mp_neg(self):
        cp = self.mp_init_copy()
        if cp.used == 0:
            return cp
        if cp.sign == _MP_ZPOS:
            cp.sign = _MP_NEG
        elif cp.sign == _MP_NEG:
            cp.sign = _MP_ZPOS
        return cp

    # Arithmetic ops.
    # TODO: Imp. in place version ?
    @staticmethod
    def mp_add(x, y):
        """Returns a new MPInt."""
        # O(n)
        w = None
        return w

    def mp_sub(self, x, y):
        # O(n)
        raise NotImplemented

    def mp_mult(self, x, y):
        # TODO: Karatsuba in numbers are large enough ?
        raise NotImplemented

    def mp_divide(self, x, y):
        raise NotImplemented




if __name__ == "__main__":
    import testing.tests
    testing.tests.run()
