# coding: utf-8

from syne.unit import Unit, Core
from syne.calc import Matrix
from syne.tools import from_plain_signal, to_plain_signal
from test.tools import get_conf


def test_core():
    core = Core(get_conf())


def test_unit():
    unit = Unit(get_conf(
        UNIT_INPUT_HEIGHT=2,
        UNIT_INPUT_WIDTH=4,
        UNIT_OUTPUT_WIDTH=4
    ))

    messages = [
        Matrix([
            from_plain_signal(i % 4, 4),
            from_plain_signal((i + 1) % 4, 4),
        ])
        for i in range(1000)
    ]

    for message in messages:
        unit.activate(message)

    message = Matrix((
        from_plain_signal(0, 4),
        from_plain_signal(1, 4),
    ))
    output_signal = unit.activate(message)
    decoded_message = unit.decode(output_signal)

    plain_message = list(map(to_plain_signal, decoded_message.rows()))
    assert plain_message == [0, 1]


