# -*- coding: utf-8 -*-

from syne.unit import Unit
from syne.tools import Buffer


class TimeUnit:
    """
    This type of unit accepts only one signal per activation, but can predict next signals
    """
    def __init__(self, conf):
        assert conf.TIME_UNIT_BASE_SIGNALS_NUMBER <= conf.UNIT_INPUT_HEIGHT

        self.conf = conf
        self.unit = Unit(conf)

        self._buffer = Buffer([], size=self.conf.UNIT_INPUT_HEIGHT)

    def activate(self, signal, learn=True):
        """
        Put signal to the unit
        :param signal: signal to activate
        :param learn: is learning enabled
        :return: output signal of this unit
        """
        self._buffer.push(signal)
        learn = learn and all(self._buffer)
        return self.unit.activate(tuple(self._buffer), learn=learn)

    def reset(self):
        """
        Forget all last signals (but not patterns).
        While unit has not enough signals, prediction is not be possible
        """
        self._buffer = Buffer([], size=self.conf.UNIT_INPUT_HEIGHT)

    def get_prediction(self):
        """
        :return: predicted signals
        """
        signals_to_predict = self.conf.UNIT_INPUT_HEIGHT - self.conf.TIME_UNIT_BASE_SIGNALS_NUMBER
        signals = list(self._buffer)[signals_to_predict:] + [None] * signals_to_predict
        restored_signals = self.unit.restore(signals)
        predicted_signals = restored_signals[-signals_to_predict:]
        return predicted_signals
