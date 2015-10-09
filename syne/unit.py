from syne.incubator import Incubator
from syne.matrix import similarity
from syne.tools import avg


class Unit(object):
    def __init__(self, conf):
        self.conf = conf

        self.incubator = Incubator(conf)
        self.core = Core(conf)

    def activate(self, message, prediction):
        """
        message: matrix
        prediction: vector
        return: vector
        """
        output_signal = self.core.activate(message, prediction)
        output_activity = avg(output_signal)

        if output_activity < self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY:
            new_patterns = self.incubator.add(message)
            self.core.add_patterns(new_patterns)
            return None

        return output_signal

    def decode(self, signal):
        return self.core.decode(signal)

    def restore(self, message):
        pass


class Core(object):
    def __init__(self, conf):
        self.conf = conf

        self._patterns = []

    def activate(self, message, prediction):
        result = []
        for pattern in self._patterns:
            activity = similarity(message, pattern)
            result.append(activity)

        # TODO: add prediction

        return result

    def decode(self, signal):
        return []

    def add_patterns(self, new_patterns):
        pass
