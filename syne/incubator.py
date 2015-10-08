from itertools import product
from collections import defaultdict


class Incubator(object):
    def __init__(self, conf):
        self.conf = conf
        self.samples = defaultdict(float)     # {sample: weight}

    def add(self, message):    # return list of Patterns (matrixes?)
        self._update_samples(message)

        new_patterns = []
        while max(self.samples.values()) >= self.conf.INCUBATOR_READY_SAMPLE_WEIGHT:
            top_samples = [sample for sample, weight in self.samples.items()]
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

    def _make_pattern(self, sample):
        pass


def make_samples(threshold, message):
    assert message, "Message can't be empty"
    assert all(len(s) == len(message[0]) for s in message), "All signals should have equal size"

    res = {}
    for impulses in product(xrange(len(message[0])), repeat=len(message)):
        values = [message[n][i] for n, i in enumerate(impulses)]
        sample = tuple(i if v >= threshold else None for v, i in zip(values, impulses))
        activity = (sum(values) / len(values))
        res[sample] = activity

    return res
