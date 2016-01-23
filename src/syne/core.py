# coding: utf-8

from syne.calc import matrix_multiply
from syne.store import Store
from synemx import Matrix


class Core(object):
    KEY = 'core'

    def __init__(self, conf, data=None):
        self.conf = conf

        patterns = map(Matrix, data['patterns']) if data else []
        pattern_weights = data['pattern_weights'] if data else []

        self._patterns_store = Store(
            patterns, pattern_weights,
            self.conf.UNIT_OUTPUT_WIDTH,
            min_weight=self.conf.UNIT_MIN_PATTERN_WEIGHT,
            max_weight=self.conf.UNIT_MAX_PATTERN_WEIGHT,
            average_weight=self.conf.UNIT_AVERAGE_PATTERN_WEIGHT
        )

    def get_data(self):
        return {
            '_key': self.KEY,
            'patterns': [p.get_data() for p in self._patterns_store.get_objects()],
            'pattern_weights': self._patterns_store.get_weights()
        }

    def activate(self, message, prediction=None, learn=True, activation_threshold=None):
        """
        Activate self with message, perform learning

        return result_signal if activated else None

        :param message: (Matrix) message to activate
        :param learn: (bool) if True learn patterns with this message
        :param activation_threshold: possibility to override conf.UNIT_ACTIVATION_THRESHOLD
        for this method
        """
        # TODO: add prediction
        result_signal = self._activate(message, activation_threshold)
        if learn and result_signal:
            self._learn(message, result_signal)

        return result_signal

    def _activate(self, message, activation_threshold=None):
        activation_threshold = activation_threshold or self.conf.UNIT_ACTIVATION_THRESHOLD

        result_signal = [0.0] * self.conf.UNIT_OUTPUT_WIDTH
        for i, pattern in enumerate(self._patterns_store.get_objects()):
            activity = message.average_similarity(pattern)
            result_signal[i] = activity

        activated = (max(result_signal) >= activation_threshold)
        return result_signal if activated else None

    def decode(self, signal, activation_threshold=None):
        assert len(signal) == self.conf.UNIT_OUTPUT_WIDTH

        candidates = []
        for activity, pattern in zip(signal, self._patterns_store.get_objects()):
            candidate = matrix_multiply(pattern, activity)
            candidate_activity = self._activate(candidate, activation_threshold)
            if candidate_activity:
                candidates.append((candidate_activity, candidate))

        if not candidates:
            return None

        return max(candidates, key=lambda item: item[0])[1]

    def add_patterns(self, new_patterns):
        for pattern in new_patterns:
            self._patterns_store.add(pattern)

    def _learn(self, message, output_signal):
        max_activity = max(output_signal)

        for i, activity in enumerate(output_signal):
            if activity == max_activity:
                self._patterns_store.increase(i)
                pattern = self._patterns_store.get_objects()[i]
                pattern.approximate(message, activity * self.conf.UNIT_LEARNING_FACTOR)

        self._patterns_store.normalize()
