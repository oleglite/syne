# coding: utf-8

from syne.core import Core, signals_similarity, pattern_learn
from syne.calc import Matrix
from test.tools import get_conf


def test_core():
    core = Core(get_conf(
        UNIT_INPUT_HEIGHT=2,
        UNIT_INPUT_WIDTH=2,
        UNIT_OUTPUT_WIDTH=10
    ))

    res = core.activate([
        [0, 0],
        [0, 0]
    ])

    assert res is None


def test_signals_similarity_zero():
    s1 = (0.0, 0.0, 0.0)
    s2 = (0.0, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 0.0

    s1 = (1.0, 0.0, 0.0)
    s2 = (0.0, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 0.0

    s1 = (1.0, 1.0, 1.0)
    s2 = (0.0, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 0.0

    s1 = (1.0, 0.0, 1.0)
    s2 = (0.0, 1.0, 0.0)
    assert signals_similarity(s1, s2) == 0.0

    s1 = (0.0, 0.5, 0.0)
    s2 = (0.5, 0.0, 0.5)
    assert signals_similarity(s1, s2) == 0.0


def test_signals_similarity_similar():
    s1 = (1.0, 0.0, 0.0)
    s2 = (1.0, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 1.0

    s1 = (1.0, 1.0, 0.0)
    s2 = (1.0, 1.0, 0.0)
    assert signals_similarity(s1, s2) == 1.0

    s1 = (0.0, 0.0, 1.0)
    s2 = (0.0, 0.0, 1.0)
    assert signals_similarity(s1, s2) == 1.0

    s1 = (0.5, 1.0, 0.0)
    s2 = (0.5, 1.0, 0.0)
    assert signals_similarity(s1, s2) == 1.0

    s1 = (0.5, 1.0, 0.01)
    s2 = (0.5, 1.0, 0.01)
    assert signals_similarity(s1, s2) == 1.0


def test_signals_similarity_partly_similar():
    s1 = (0.5, 0.0, 0.0)
    s2 = (0.5, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 0.5

    s1 = (0.5, 0.5, 0.0)
    s2 = (0.5, 0.5, 0.0)
    assert signals_similarity(s1, s2) == 0.5

    s1 = (0.5, 0.5, 0.0)
    s2 = (0.5, 0.0, 0.0)
    assert signals_similarity(s1, s2) == 0.25


def test_pattern_learn_nothing():
    message = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])
    pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])
    intensity = 1.0
    expected_pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])

    pattern_learn(message, pattern, intensity)
    assert pattern == expected_pattern


def test_pattern_learn_zero_intensity():
    message = Matrix([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])
    pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])
    intensity = 0.0
    expected_pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])

    pattern_learn(message, pattern, intensity)
    assert pattern == expected_pattern


def test_pattern_learn_max_intensity():
    message = Matrix([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])
    pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])
    intensity = 1.0
    expected_pattern = Matrix([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])

    pattern_learn(message, pattern, intensity)
    assert pattern == expected_pattern


def test_pattern_learn_some_intensity():
    message = Matrix([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])
    pattern = Matrix([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])
    intensity = 0.1

    expected_pattern = Matrix([
        [0.9, 0.0, 0.1],
        [0.9, 0.1, 0.0],
    ])
    pattern_learn(message, pattern, intensity)
    assert pattern == expected_pattern

    expected_pattern = Matrix([
        [0.819, 0.0, 0.19],
        [0.819, 0.19, 0.0],
    ])
    pattern_learn(message, pattern, intensity)
    assert pattern == expected_pattern
