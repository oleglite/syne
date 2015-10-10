# coding: utf-8

from syne.calc import Matrix
from syne.incubator import Incubator, make_samples


def get_conf(**kwargs):
    # default conf for tests
    class conf:
        UNIT_INPUT_WIDTH = 2
        UNIT_INPUT_HEIGHT = 2

        INCUBATOR_ACTIVITY_THRESHOLD = 0.5
        INCUBATOR_READY_SAMPLE_WEIGHT = 1
        INCUBATOR_MIN_SAMPLE_IMPULSES = 1
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT = 0.7
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY = 0.6

    conf.__dict__.update(kwargs)

    return conf


def test_make_samples():
    samples = make_samples(0.5, [
        [0.1, 0.7],
        [0.9, 0.3],
    ])

    assert dict(samples) == {
        (None, 0): 0.5,     # 0.1 0.9
        (None, None): 0.2,  # 0.1 0.3
        (1, 0): 0.8,        # 0.7 0.9
        (1, None): 0.5,     # 0.7 0.3
    }


def test_incubator_create_samples():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=999,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
    ))
    result = incubator.add([
        [0.0, 1.0],
        [1.0, 0.0],
    ])
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
    result = incubator.add([
        [0.0, 1.0],
        [1.0, 0.0],
    ])
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
    result = incubator.add([
        [0.0, 1.0],
        [1.0, 0.0],
    ])
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


def test_incubator_create_pattern_from_several_samples():
    incubator = Incubator(get_conf(
        INCUBATOR_READY_SAMPLE_WEIGHT=1,   # doesn't create patterns
        INCUBATOR_ACTIVITY_THRESHOLD=0.5,
        INCUBATOR_MIN_SAMPLE_IMPULSES=1,
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT=0.7,
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY=0.3,
    ))
    result = incubator.add([
        [0.0, 1.0],
        [1.0, 0.0],
    ])

    # braking add (0.7, sim_weight / top_weight * base_weight)
    value = (0.7 + 0.3 * (0.5 / 1.0 * 0.7))

    assert result == [
        Matrix([
            [0.0, value],
            [value, 0.0],
        ])
    ]
    assert incubator.get_samples() == {}
