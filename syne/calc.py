
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

        self.data = list(map(list, data))

    @classmethod
    def create(cls, w, h, values=0.0):
        return cls([[values] * w for _ in xrange(h)])

    def set(self, y, x, value):
        self.data[y][x] = value

    def get(self, y, x):
        return self.data[y][x]

    def row(self, y):
        return self.data[y]

    def col(self, x):
        return list(v[x] for v in self.data)


def matrix_similarity(m1, m2):
    return 0.0


def list_similarity(l1, l2):
    return 0.0


def braking_add(a, b):
    return a + (1 - b) * a