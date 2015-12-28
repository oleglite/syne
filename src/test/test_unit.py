# coding: utf-8

from syne.unit import Unit, Core
from syne.calc import Matrix
from syne.tools import from_plain_signal
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
        for i in range(100)
    ]

    for message in messages:
        unit.activate(message)

    message = Matrix((
        from_plain_signal(0, 4),
        from_plain_signal(1, 4),
    ))
    print(unit.activate(message))

