# coding: utf-8

from syne.calc import matrix_similarity, matrix_multiply
from syne.store import Store


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

    def activate(self, message, prediction=None):
        """
        Activate self with message, perform learning

        return result_signal if activated else None
        """
        # TODO: add prediction
        result_signal = self._activate(message)
        if result_signal:
            self._learn(result_signal)

        return result_signal

    def _activate(self, message):
        result_signal = [0.0] * self.conf.UNIT_OUTPUT_WIDTH
        for i, pattern in enumerate(self._patterns_store.get_objects()):
            activity = matrix_similarity(message, pattern)
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
