from itertools import product
from collections import defaultdict

from syne.calc import similarity, braking_add, Matrix
from syne.tools import avg


class Incubator(object):
    KEY = 'incubator'

    def __init__(self, conf, samples=None, data=None):
        self.conf = conf
        self._samples = defaultdict(float)     # {sample: weight}

        if data:
            self._samples.update(data['samples'])
        elif samples:
            self._samples.update(samples)

    def get_samples(self):
        return dict(self._samples)

    def get_data(self):
        return {
            '_key': self.KEY,
            'samples': dict(self._samples)
        }

    def add(self, message):
        """
        Add message to incubator. The main method of incubator.


        :param message: tuple of samples
        :return: list of Patterns (matrixes?)
        """
        self._update_samples(message)

        new_patterns = []
        while True:
            max_weight = max(self._samples.values()) if self._samples else 0
            if max_weight < self.conf.INCUBATOR_READY_SAMPLE_WEIGHT:
                break

            top_samples = [sample for sample, weight in self._samples.items()
                           if weight == max_weight]
            top_sample = top_samples[0]     # TODO: use random
            new_patterns.append(self._make_pattern(top_sample))

        return new_patterns

    def _update_samples(self, message):
        min_impulses = self.conf.INCUBATOR_MIN_SAMPLE_IMPULSES

        samples = make_samples(self.conf.INCUBATOR_IMPULSE_ACTIVITY_THRESHOLD, message)

        # filter samples with lots of Nones
        samples = ((s, a) for s, a in samples if len(s) - s.count(None) >= min_impulses)

        # leave only best copy of each sample
        result_samples = {}
        for sample, activity in samples:
            if result_samples.get(sample, 0) < activity:
                result_samples[sample] = activity

        for sample, activity in result_samples.items():
            self._samples[sample] += activity

    def _make_pattern(self, base_sample):
        base_sample_weight = self._samples.pop(base_sample)
        base_weight = self.conf.INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT

        # find similar samples
        similar_samples = {}
        for sample, sample_weight in dict(self._samples).items():
            activity = similarity(base_sample, sample)
            if activity >= self.conf.INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY:
                similar_samples[sample] = sample_weight
                del self._samples[sample]

        # create pattern from base sample
        pattern = Matrix.create(self.conf.UNIT_INPUT_HEIGHT, self.conf.UNIT_INPUT_WIDTH)
        for y, impulse in enumerate(base_sample):
            if impulse is not None:
                pattern.set(impulse, y, base_weight)

        # add similar samples to pattern
        for sample, sample_weight in similar_samples.items():
            adding_weight = sample_weight / base_sample_weight * base_weight
            for y, impulse in enumerate(sample):
                if impulse is not None:
                    new_weight = braking_add(pattern.get(impulse, y), adding_weight)
                    pattern.set(impulse, y, new_weight)

        return pattern


def make_samples(threshold, message):
    assert message, "Message can't be empty"

    active_impulses = [
        [i for i, a in enumerate(row) if a >= threshold] + [None]
        for row in message.rows()
    ]

    for sample in product(*active_impulses):
        values = [message.get(x, y) if x is not None else 0 for y, x in enumerate(sample)]
        activity = avg(values)
        if activity:
            yield sample, activity
