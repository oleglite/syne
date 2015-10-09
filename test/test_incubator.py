# coding: utf-8

from syne.incubator import Incubator, make_samples


class test_conf:
    UNIT_INPUT_WIDTH = 2
    UNIT_INPUT_HEIGHT = 2

    INCUBATOR_ACTIVITY_THRESHOLD = 0.5
    INCUBATOR_READY_SAMPLE_WEIGHT = 1
    INCUBATOR_MIN_SAMPLE_IMPULSES = 1
    INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT = 0.7
    INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY = 0.6


def test_incubator():
    incubator = Incubator(test_conf)
    result = incubator.add([
        [0.0, 1.0],
        [1.0, 0.0],
    ])
    assert result == []


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