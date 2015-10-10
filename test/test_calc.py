# coding: utf-8

from syne.calc import similarity, matrix_similarity, Matrix


def test_similarity():
    sim = similarity(
        [0.1, 0.1],
        [0.1, 0.1],
    )
    assert 0.9999 < sim <= 1.0, 'equal lists'

    sim = similarity(
        [1.0, 1.0],
        [0.0, 0.0],
    )
    assert 0.0 <= sim < 0.00001, 'max difference'

    sim1 = similarity(
        [0.1, 0.1],
        [0.2, 0.1],
    )
    sim2 = similarity(
        [0.1, 0.1],
        [0.2, 0.2],
    )
    assert 0.01 < sim1 < 0.99
    assert 0.01 < sim2 < 0.99
    assert sim1 > sim2


def test_matrix_similarity():
    sim = matrix_similarity(
        Matrix([
            [0.1, 0.1],
            [0.1, 0.1],
        ]),
        Matrix([
            [0.1, 0.1],
            [0.1, 0.1],
        ]),
    )
    assert 0.9999 < sim <= 1.0, 'equal matrixes'

    sim = matrix_similarity(
        Matrix([
            [0.0, 0.0],
            [0.0, 0.0],
        ]),
        Matrix([
            [1.0, 1.0],
            [1.0, 1.0],
        ]),
    )
    assert 0.0 <= sim < 0.00001, 'max difference'

    sim1 = matrix_similarity(
        Matrix([
            [0.1, 0.1],
            [0.1, 0.1],
        ]),
        Matrix([
            [0.1, 0.1],
            [0.2, 0.1],
        ]),
    )
    sim2 = matrix_similarity(
        Matrix([
            [0.1, 0.1],
            [0.1, 0.1],
        ]),
        Matrix([
            [0.1, 0.2],
            [0.2, 0.1],
        ]),
    )
    assert 0.01 < sim1 < 0.99
    assert 0.01 < sim2 < 0.99
    assert sim1 > sim2
