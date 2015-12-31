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
        if None in signals:
            learn = False

        activation_threshold = self._get_activation_threshold_for_signals(signals)
        message_matrix = self._make_message(signals)

        output_signal = self.core.activate(
            message_matrix, prediction, learn=learn, activation_threshold=activation_threshold
        )
        output_activity = max(output_signal) if output_signal else 0

        if learn and output_activity < self.conf.UNIT_ACTIVATION_THRESHOLD:
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
        assert len(signals) == self.conf.UNIT_INPUT_HEIGHT

        if not any(signal is None for signal in signals):
            return signals

        activation_threshold = self._get_activation_threshold_for_signals(signals)
        message_matrix = self._make_message(signals)
        output_signal = self.core.activate(
            message_matrix, learn=False, activation_threshold=activation_threshold
        )

        # because of empy signals in message, output signal is lowered, need to normalize it
        normalization_factor = len(signals) / signals.count(None)
        normalized_output_signal = tuple(a * normalization_factor for a in output_signal)
        assert all(0 <= a <= 1 for a in normalized_output_signal)

        decoded_message = self.core.decode(normalized_output_signal)

        if not decoded_message:
            print('WARNING: failed to restore message', message_matrix)
            return message_matrix.get_data()

        decoded_signals = decoded_message.get_data()
        result_signals = tuple(s or decoded_signals[i] for i, s in enumerate(signals))
        return result_signals

    def _get_activation_threshold_for_signals(self, signals):
        return self.conf.UNIT_ACTIVATION_THRESHOLD * (1 - (signals.count(None) / len(signals)))

    def _make_message(self, signals):
        message_signals = signals
        if None in signals:
            default_signal = (0,) * self.conf.UNIT_INPUT_WIDTH
            message_signals = tuple(s or default_signal for s in signals)

        return Matrix(message_signals)
