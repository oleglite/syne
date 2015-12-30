# coding: utf-8

from syne.calc import (similarity, Matrix, limited_add, matrix_multiply,
                       braking_add, braking_sub)


def test_similarity():
    sim = similarity(
        [1, 1],
        [1, 1],
    )
    assert 0.9999 < sim <= 1.0, 'equal lists'

    sim = similarity(
        [1, 1],
        [0, 0],
    )
    assert 0.0 <= sim < 0.00001, 'max difference'

    sim = similarity(
        [1, 1],
        [2, 1],
    )
    assert 0.49 < sim < 0.51


def test_limited_add():
    assert limited_add(2, 3, 0, 10) == 5
    assert limited_add(2, 3, 7, 10) == 7
    assert limited_add(2, 3, 0, 1) == 1


def test_braking_add():
    assert braking_add(0, 0) == 0
    assert braking_add(1, 1) == 1
    assert braking_add(1, 0) == 1
    assert braking_add(0, 1) == 1
    assert braking_add(0.5, 0.5) == 0.75
    assert braking_add(0.1, 0.1) == 0.19
    assert braking_add(0.9, 0.1) == 0.91


def test_braking_sub():
    assert braking_sub(0, 0) == 0
    assert braking_sub(1, 1) == 0
    assert braking_sub(1, 0) == 1
    assert braking_sub(0, 1) == 0
    assert braking_sub(0.5, 0.5) == 0.25
    assert braking_sub(0.9, 0.1) == 0.81


def test_matrix_multiply():
    m = Matrix([
        [0.0, 0.1],
        [0.6, 1.0],
    ])
    res = Matrix([
        [0.0, 0.05],
        [0.3, 0.5],
    ])
    assert matrix_multiply(m, 0.5) == res

