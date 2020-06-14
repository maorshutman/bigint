import numpy as np
import torch


class BigIntTensor(torch.Tensor):
    """
    """
    def __new__(cls, x, bits, sign=1, *args, **kwargs):
        if type(x) == int:
            x = cls._py_int_to_tensor(x, bits)
        elif type(x) == list:
            x = cls._zero_pad(x, bits)
        assert bits == len(x)

        # Tensor size will be 1 x bits.
        return super().__new__(cls, [x], *args, **kwargs)

    def __init__(self, x, bits, sign=1):
        self.alloc = bits

        # User can give list and sign (1/positive by default)
        # or python int with sign
        self.sign = sign  # if given as a list
        if type(x) == int:
            self.sign = self._sign(x)

        if type(x) == list:
            self.used = self._used_in_list(x)
        elif type(x) == int:
            self.used = self._used_in_list(self._py_int_to_tensor(x, self.alloc))

    @staticmethod
    def add(x, y):
        # use as w = x + y
        # pad both numbers
        # write the loop with a cary
        w = None
        return w

    def sub(self, x, y):
        raise NotImplemented

    def mult(self, x, y):
        raise NotImplemented

    def divide(self, x, y):
        raise NotImplemented

    @staticmethod
    def _py_int_to_tensor(x, bits):
        bin = np.binary_repr(x)
        bin_out = []
        for c in bin:
            if c in ['0', '1']:
                bin_out.append(int(c))

        if bits <= len(bin_out):
            raise Exception("Not enough bits for given integer.")

        # Pad with zeros.
        bin_out = [0] * (bits - len(bin_out)) + bin_out
        assert len(bin_out) == bits

        return bin_out

    @staticmethod
    def _sign(x):
        return int(x >= 0)

    @staticmethod
    def _used_in_list(x):
        assert type(x) == list
        num_bits = len(x)
        i = 0
        while (i != num_bits) and (x[i] != 1):
            i += 1
        return num_bits - i

    @staticmethod
    def _used_in_py_int(x):
        used = 0
        while x != 0:
            used += 1
            x = x // 2
        return used

    @staticmethod
    def _zero_pad(x, alloc):
        if alloc <= len(x):
            raise Exception("Not enough bits for given integer.")
        bin_out = [0] * (alloc - len(x)) + x
        assert len(bin_out) == alloc
        return bin_out


x = BigIntTensor([0, 1, 1], bits=8)
y = BigIntTensor(int(-7), bits=8)


print(x, x.sign, x.used, x.shape)
print(y, y.sign, y.used, y.shape)
