# coding: utf-8

from syne.calc import Matrix
from syne.incubator import Incubator, make_samples
from test.tools import get_conf


def test_make_samples():
    samples = make_samples(0.5, Matrix([
        [0.1, 0.7],
        [0.9, 0.3],
    ]))

    assert dict(samples) == {
        (None, 0): 0.45,    # 0.1 0.9
        (None, None): 0,    # 0.1 0.3
        (1, 0): 0.8,        # 0.7 0.9
        (1, None): 0.35,    # 0.7 0.3
    }


def test_make_samples_2x3():
    samples = make_samples(0.5, Matrix([
        [0.0, 0.9],
        [0.3, 0.3],
        [0.6, 0.9],
    ]))

    # [None, 1],
    # [None, None],
    # [0, 1],

    expected_samples = [
        ((None, None, 0), 0.2), # 0.0 0.3 0.6
        ((None, None, 1), 0.3), # 0.0 0.3 0.9

        ((None, None, 0), 0.2), # 0.0 0.3 0.6
        ((None, None, 1), 0.3), # 0.0 0.3 0.9

        ((1, None, 0), 0.5),    # 0.9 0.3 0.6
        ((1, None, 1), 0.6),    # 0.9 0.3 0.9

        ((1, None, 0), 0.5),    # 0.9 0.3 0.6
        ((1, None, 1), 0.6),    # 0.9 0.3 0.9
    ]

    for sample, weight in samples:
        found = False
        for expected_sample, expected_weight in list(expected_samples):
            if sample == expected_sample and abs(weight - expected_weight) < 0.0001:
                expected_samples.remove((expected_sample, expected_weight))
                found = True
                break
        if not found:
            assert False, 'unexpected sample %s with weight %s' % (sample, weight)


def test_incubator_create_samples():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=999,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
    ))
    result = incubator.add(Matrix([
        [0.0, 1.0],
        [1.0, 0.0],
    ]))
    assert result == []
    assert incubator.get_samples() == {
        (None, 0): 0.5,
        (1, 0): 1.0,
        (1, None): 0.5,
    }


def test_incubator_create_samples_min_impulses_filter():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=999,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=2,
    ))
    result = incubator.add(Matrix([
        [0.0, 1.0],
        [1.0, 0.0],
    ]))
    assert result == []
    assert incubator.get_samples() == {
        (1, 0): 1.0,
    }


def test_incubator_create_pattern():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=1,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT=0.7,
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY=0.6,
    ))
    result = incubator.add(Matrix([
        [0.0, 1.0],
        [1.0, 0.0],
    ]))
    assert result == [
        Matrix([
            [0.0, 0.7],
            [0.7, 0.0],
        ])
    ]
    assert incubator.get_samples() == {
        (None, 0): 0.5,
        (1, None): 0.5,
    }


def test_incubator_create_pattern_2x3():
    incubator = Incubator(get_conf(
        UNIT_INPUT_HEIGHT=2,
        UNIT_INPUT_WIDTH=3,
        INCUBATOR_READY_SAMPLE_WEIGHT=1,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT=0.7,
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY=0.6,
    ))
    result = incubator.add(Matrix([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
    ]))
    assert result == [
        Matrix([
            [0.0, 0.7, 0.0],
            [0.0, 0.0, 0.7],
        ]),
        Matrix([
            [0.0, 0.7, 0.0],
            [0.7, 0.0, 0.0],
        ])
    ]
    samples = incubator.get_samples()
    assert samples == {
        (None, 0): 0.5,
        (None, 2): 0.5,
        (1, None): 0.5,
    }


def test_incubator_create_pattern_from_several_samples():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=0.9,
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT=0.7,
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY=0.3,
    ))
    result = incubator.add(Matrix([
        [0.0, 1.0],
        [1.0, 0.0],
    ]))

    # braking add (0.7, sim_weight / top_weight * base_weight)
    value = (0.7 + 0.3 * (0.5 / 1.0 * 0.7))

    assert result == [
        Matrix([
            [0.0, value],
            [value, 0.0],
        ])
    ]
    assert incubator.get_samples() == {}
