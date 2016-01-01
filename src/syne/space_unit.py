# -*- coding: utf-8 -*-

from syne.unit import Unit


class SpaceUnit:
    def __init__(self, conf):
        self.conf = conf
        self.unit = Unit(conf)

    def activate(self, signals, learn=True):
        return self.unit.activate(signals, learn=learn)

    def decode(self, signal):
        return self.unit.decode(signal)
