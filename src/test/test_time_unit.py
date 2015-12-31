# -*- coding: utf-8 -*-

from syne.time_unit import TimeUnit
from syne.tools import from_plain_signal, to_plain_signal
from test.tools import get_conf


def test_time_unit_prediction():
    unit = TimeUnit(get_conf(
        UNIT_INPUT_HEIGHT=2,
        UNIT_INPUT_WIDTH=4,
        UNIT_OUTPUT_WIDTH=4,
        TIME_UNIT_BUFFER_SIZE=1
    ))

    # learning
    signals_to_learn = [
        from_plain_signal(i % 4, 4)
        for i in range(100)
    ]
    for signal in signals_to_learn:
        unit.activate(signal)

    # set base signals for prediction
    signals = [
        from_plain_signal(0, 4),
    ]
    unit.reset()
    for signal in signals:
        unit.activate(signal)

    # predict
    expected_prediction = from_plain_signal(1, 4)
    prediction = unit.get_prediction()

    assert to_plain_signal(prediction[0]) == to_plain_signal(expected_prediction)
