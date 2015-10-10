from itertools import izip, chain
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

        self.w = len(data[0])
        self.h = len(data)

        self._data = list(map(list, data))

    @classmethod
    def create(cls, w, h, values=0.0):
        return cls([[values] * w for _ in xrange(h)])

    def set(self, y, x, value):
        self._data[y][x] = value

    def get(self, y, x):
        return self._data[y][x]

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

    def __repr__(self):
        return 'Matrix(%s)' % pformat(self._data)


def matrix_similarity(m1, m2):
    assert m1.w == m2.w and m1.h == m2.h, 'Matrixes should have same size'

    it1 = chain(*m1.get_data())
    it2 = chain(*m2.get_data())

    # compare matrix cells with same coords
    difs = ((x - y) ** 2 for x, y in izip(it1, it2))
    res = 1 - avg(difs) ** 0.5
    assert 0 <= res <= 1, 'Similarity should be in range from 0 to 1'
    return res


def similarity(it1, it2):
    return avg(int(x == y) for x, y in izip(it1, it2))


def braking_add(a, b):
    return a + (1 - a) * b
