from syne.tools import avg
from synemx import Matrix


def similarity(it1, it2):
    return avg(int(x == y) for x, y in zip(it1, it2))


def braking_add(a, b):
    assert 0 <= a <= 1
    assert 0 <= b <= 1
    return a + (1 - a) * b


def braking_sub(a, b):
    assert 0 <= a <= 1
    assert 0 <= b <= 1
    return a - a * b


def limited_add(a, b, min_result, max_result):
    return max(min(a + b, max_result), min_result)


def matrix_multiply(m, factor):
    assert 0 <= factor <= 1, 'only fractional factors are supproted'

    def _mult_row(row, x):
        return [v * x for v in row]

    return Matrix([_mult_row(row, factor) for row in m.get_data()])


def matrix_map(func, m1, m2):
    assert m1.w == m2.w and m1.h == m2.h, 'Matrixes must have same size'

    return Matrix([map(func, v1, v2) for v1, v2 in zip(m1.get_data(), m2.get_data())])
