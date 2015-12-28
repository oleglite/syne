# coding: utf-8


def get_conf(**kwargs):
    # default conf for tests
    class conf:
        UNIT_ACTIVE_SIGNAL_ACTIVITY = 0.5
        UNIT_INPUT_HEIGHT = 2
        UNIT_INPUT_WIDTH = 2
        UNIT_OUTPUT_WIDTH = 5
        UNIT_MAX_PATTERN_WEIGHT = 10
        UNIT_MIN_PATTERN_WEIGHT = -10
        UNIT_AVERAGE_PATTERN_WEIGHT = 4

        INCUBATOR_ACTIVITY_THRESHOLD = 0.5
        INCUBATOR_READY_SAMPLE_WEIGHT = 1
        INCUBATOR_MIN_SAMPLE_IMPULSES = 1
        INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT = 0.7
        INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY = 0.6

    for kwarg, value in kwargs.items():
        setattr(conf, kwarg, value)

    return conf
