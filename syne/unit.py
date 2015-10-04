from syne.incubator import Incubator


class Unit:
    def __init__(self, conf):
        self.conf = conf

        self.incubator = Incubator(conf)

    def activate(self, signal):
        pass

    def decode(self, message):
        pass

    def restore(self, message):
        pass
