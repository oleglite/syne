from syne.core import Core
from syne.incubator import Incubator
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
        return: vector or None
        """
        output_signal = self.core.activate(message, prediction)
        output_activity = avg(output_signal)

        if output_activity < self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY:
            new_patterns = self.incubator.add(message)
            self.core.add_patterns(new_patterns)
            return None

        return output_signal

    def decode(self, signal):
        """
        signal: vector
        return: matrix or None
        """
        return self.core.decode(signal)

    def restore(self, message):
        if not any(signal is None for signal in message):
            return message

        # TODO: first need to implement in Core to allow None signals in message
        pass
