# coding: utf-8

from itertools import chain, starmap

from syne.calc import matrix_multiply
from syne.store import Store
from syne.tools import avg


class Core(object):
    def __init__(self, conf):
        self.conf = conf

        self._patterns_store = Store(
            [], [],
            self.conf.UNIT_OUTPUT_WIDTH,
            min_weight=self.conf.UNIT_MIN_PATTERN_WEIGHT,
            max_weight=self.conf.UNIT_MAX_PATTERN_WEIGHT,
            average_weight=self.conf.UNIT_AVERAGE_PATTERN_WEIGHT
        )

    def activate(self, message, prediction=None, learn=True):
        """
        Activate self with message, perform learning

        return result_signal if activated else None

        :param message: (Matrix) message to activate
        :param learn: (bool) if True learn patterns with this message
        """
        # TODO: add prediction
        result_signal = self._activate(message)
        if learn and result_signal:
            self._learn(result_signal)

        return result_signal

    def _activate(self, message):
        result_signal = [0.0] * self.conf.UNIT_OUTPUT_WIDTH
        for i, pattern in enumerate(self._patterns_store.get_objects()):
            activity = avg(starmap(signals_similarity, zip(message.rows(), pattern.rows())))
            result_signal[i] = activity

        activated = any(a >= self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY for a in result_signal)
        return result_signal if activated else None

    def decode(self, signal):
        assert len(signal) == self.conf.UNIT_OUTPUT_WIDTH

        candidates = []
        for activity, pattern in zip(signal, self._patterns_store.get_objects()):
            candidate = matrix_multiply(pattern, activity)
            candidate_activity = self._activate(candidate)
            if candidate_activity:
                candidates.append((candidate_activity, candidate))

        if not candidates:
            return None

        return max(candidates, key=lambda item: item[0])[1]

    def add_patterns(self, new_patterns):
        for pattern in new_patterns:
            self._patterns_store.add(pattern)

    def _learn(self, output_signal):
        for i, activity in enumerate(output_signal):
            if activity >= self.conf.UNIT_ACTIVE_SIGNAL_ACTIVITY:
                self._patterns_store.increase(i)

        self._patterns_store.normalize()


def signals_similarity(s1, s2):
    """
    :param s1: signal 1
    :param s2: signal 2
    :return: signals similarity
    """
    s_min = sum(map(min, zip(s1, s2)))
    s_max = sum(map(max, zip(s1, s2)))
    limit = max(chain(s1, s2))
    return (limit * s_min / s_max) if s_max else 0.0
