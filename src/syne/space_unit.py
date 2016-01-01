# -*- coding: utf-8 -*-

from syne.unit import Unit


class SpaceUnit:
    KEY = 'space_unit'

    def __init__(self, conf, data=None):
        self.conf = conf

        if data:
            self.unit = Unit(conf, data=data['unit'])
        else:
            self.unit = Unit(conf)

    def get_data(self):
        return {
            '_key': self.KEY,
            'unit': self.unit.get_data(),
        }

    def activate(self, signals, learn=True):
        return self.unit.activate(signals, learn=learn)

    def decode(self, signal):
        return self.unit.decode(signal)
