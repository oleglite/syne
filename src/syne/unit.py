from syne.core import Core
from syne.incubator import Incubator
from syne.tools import avg
from syne.calc import Matrix


class Unit(object):
    """
    Note: Input for Unit is signals but not Matrix object because signal can be None
    """
    def __init__(self, conf):
        self.conf = conf

        self.incubator = Incubator(conf)
        self.core = Core(conf)

    def activate(self, signals, prediction=None):
        """
        message: matrix
        prediction: vector
        return: vector or None

        :param signals: any iterable with input signals
        :return (tuple) output signal
        """
        assert all(signals), "Can't activate None signals"
        message_matrix = Matrix(signals)

        output_signal = self.core.activate(message_matrix, prediction)
        output_activity = avg(output_signal) if output_signal else 0

        if output_activity < self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY:
            new_patterns = self.incubator.add(message_matrix)
            self.core.add_patterns(new_patterns)
            return None

        return output_signal

    def decode(self, signal):
        """
        :param signal: list of activities
        :return tuple of signals or None
        """
        assert signal, "Can't decode None siganl"

        message = self.core.decode(signal)
        return message.get_data() if message else None

    def restore(self, signals):
        if not any(signal is None for signal in signals):
            return signals

        # TODO: first need to implement in Core to allow None signals in message
        pass
