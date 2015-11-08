# coding: utf-8

from syne.core import Core
from test.tools import get_conf


def test_core():
    core = Core(get_conf(
        UNIT_INPUT_WIDTH=2,
        UNIT_INPUT_HEIGHT=2,
        UNIT_OUTPUT_HEIGHT=10
    ))

    res = core.activate([
        [0, 0],
        [0, 0]
    ])

    assert res is None
