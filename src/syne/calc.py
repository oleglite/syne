from itertools import chain
from pprintpp import pformat

from syne.tools import avg


class Matrix:
    def __init__(self, data):
        """
        example:
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        h = 2
        w = 3
        """

        assert all(len(v) == len(data[0]) for v in data)

        self.h = len(data)
        self.w = len(data[0])

        self._data = list(map(list, data))

    @classmethod
    def create(cls, h, w, values=0.0):
        return cls([[values] * w for _ in range(h)])

    def set(self, x, y, value):
        self._data[x][y] = value

    def get(self, x, y):
        return self._data[x][y]

    def row(self, y):
        return self._data[y]

    def col(self, x):
        return list(v[x] for v in self._data)

    def get_data(self):
        return self._data

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self._data == other.get_data()

    def __len__(self):
        return self.h

    def __repr__(self):
        return 'Matrix(%s)' % pformat(self._data)


def matrix_similarity(m1, m2):
    assert m1.w == m2.w and m1.h == m2.h, 'Matrixes should have same size'

    it1 = chain(*m1.get_data())
    it2 = chain(*m2.get_data())

    # compare matrix cells with same coords
    difs = ((x - y) ** 2 for x, y in zip(it1, it2))
    res = 1 - avg(difs) ** 0.5
    assert 0 <= res <= 1, 'Similarity should be in range from 0 to 1'
    return res


def similarity(it1, it2):
    return avg(int(x == y) for x, y in zip(it1, it2))


def braking_add(a, b):
    return a + (1 - a) * b


def limited_add(a, b, min_result, max_result):
    return max(min(a + b, max_result), min_result)


def matrix_multiply(m, factor):
    assert 0 <= factor <= 1, 'only fractional factors are supproted'

    def _mult_row(row, x):
        return [v * x for v in row]

    return Matrix([_mult_row(row, factor) for row in m.get_data()])


def matrix_map(func, m1, m2):
    assert m1.w == m2.w and m1.h == m2.h, 'Matrixes should have same size'

    return Matrix([map(func, v1, v2) for v1, v2 in zip(m1.get_data(), m2.get_data())])