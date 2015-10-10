from itertools import product
from collections import defaultdict

from syne.calc import similarity, braking_add, Matrix
from syne.tools import avg


class Incubator(object):
    def __init__(self, conf):
        self.conf = conf
        self.samples = defaultdict(float)     # {sample: weight}

    def add(self, message):    # return list of Patterns (matrixes?)
        self._update_samples(message)

        new_patterns = []
        while True:
            max_weight = max(self.samples.itervalues())
            if max_weight < self.conf.INCUBATOR_READY_SAMPLE_WEIGHT:
                break

            top_samples = [sample for sample, weight in self.samples.items()
                           if weight == max_weight]
            top_sample = top_samples[0]     # TODO: use random
            new_patterns.append(self._make_pattern(top_sample))

        return new_patterns

    def _update_samples(self, message):
        all_samples = make_samples(self.conf.INCUBATOR_ACTIVITY_THRESHOLD, message)

        # leave only best copy of each binary sample
        result_samples = {}
        for sample, activity in all_samples.iteritems():
            if len(sample) - sample.count(None) < self.conf.INCUBATOR_MIN_SAMPLE_IMPULSES:
                continue

            if result_samples.get(sample, 0) < activity:
                result_samples[sample] = activity

        for sample, activity in result_samples.iteritems():
            self.samples[sample] += activity

    def _make_pattern(self, base_sample):
        base_sample_weight = self.samples.pop(base_sample)
        base_weight = self.conf.INCUBATOR_NEW_PATTERN_IMPULSE_WEIGHT

        # find similar samples
        similar_samples = {}
        for sample, sample_weight in self.samples.items():
            activity = similarity(base_sample, sample)
            if activity >= self.conf.INCUBATOR_NEW_PATTERN_SIMILAR_SAMPLES_ACTIVITY:
                similar_samples[sample] = sample_weight
                del self.samples[sample]

        # create pattern from base sample
        pattern = Matrix.create(self.conf.UNIT_INPUT_WIDTH, self.conf.UNIT_INPUT_HEIGHT)
        for x, impulse in enumerate(base_sample):
            if impulse:
                pattern.set(impulse, x, base_weight)

        # add similar samples to pattern
        for sample, sample_weight in similar_samples.iteritems():
            adding_weight = sample_weight / base_sample_weight * base_weight
            for x, impulse in enumerate(sample):
                if impulse:
                    new_weight = braking_add(pattern.get(impulse, x), adding_weight)
                    pattern.set(impulse, x, new_weight)

        return pattern


def make_samples(threshold, message):
    assert message, "Message can't be empty"
    assert all(len(s) == len(message[0]) for s in message), "All signals should have equal size"

    res = {}
    for impulses in product(xrange(len(message[0])), repeat=len(message)):
        values = [message[n][i] for n, i in enumerate(impulses)]
        sample = tuple(i if v >= threshold else None for v, i in zip(values, impulses))
        activity = avg(values)
        res[sample] = activity

    return res
