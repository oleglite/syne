from syne.core import Core
from syne.incubator import Incubator
from syne.calc import Matrix


class Unit(object):
    """
    Note: Input for Unit is signals but not Matrix object because signal can be None
    """
    def __init__(self, conf):
        self.conf = conf

        self.incubator = Incubator(conf)
        self.core = Core(conf)

    def activate(self, signals, prediction=None, learn=True):
        """
        message: matrix
        prediction: vector
        return: vector or None

        :param signals: any iterable with input signals
        :param learn: (bool) if True learn patterns with this signals
        :return (tuple) output signal
        """
        assert all(signals), "Can't activate None signals"
        message_matrix = Matrix(signals)

        output_signal = self.core.activate(message_matrix, prediction, learn=learn)
        output_activity = max(output_signal) if output_signal else 0

        if learn and output_activity < self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY:
            new_patterns = self.incubator.add(message_matrix)
            self.core.add_patterns(new_patterns)
            return None

        return output_signal

    def decode(self, signal):
        """
        :param signal: list of activities
        :return tuple of signals or None
        """
        assert signal, "Can't decode None signal"

        message = self.core.decode(signal)
        return message.get_data() if message else None

    def restore(self, signals):
        if not any(signal is None for signal in signals):
            return signals

        default_signal = (0,) * self.conf.UNIT_INPUT_WIDTH
        filled_signals = tuple(s or default_signal for s in signals)

        output_signal = self.activate(filled_signals, learn=False)
        decoded_signals = self.decode(output_signal)

        result_signals = tuple(s or decoded_signals[i] for i, s in enumerate(signals))
        return result_signals
