from itertools import product
from collections import defaultdict


class Incubator:
    def __init__(self, conf):
        self.conf = conf
        self.samples = defaultdict(float)     # {binary_sample: weight}

    def add(self, message):    # return list of Patterns (matrixes?)
        self._update_samples(message)

        new_patterns = []
        while max(self.samples.values()) >= self.conf.INCUBATOR_READY_SAMPLE_WEIGHT:
            top_samples = [sample for sample, weight in self.samples.items()]
            top_sample = top_samples[0]     # TODO: use random
            new_patterns.append(self._make_pattern(top_sample))

        return new_patterns

    def _update_samples(self, message):
        original_samples = product(*message)    # TODO!!!!  save impulses!
        
        # get binary representation for each sample
        all_samples = {
            sample: self._make_binary_sample(sample)
            for sample in original_samples
        }

        # leave only best copy of each binary sample
        binary_samples = {}
        for sample, binary_sample in all_samples.items():
            sample_activity = sum(sample) / len(sample)
            if binary_samples.get(binary_sample, 0) < sample_activity:
                binary_samples[binary_sample] = sample_activity

        for binary_sample, sample_activity in binary_samples.items():
            self.samples[binary_sample] += sample_activity

    def _make_binary_sample(self, sample):
        return tuple(int(a >= self.conf.INCUBATOR_ACTIVITY_THRESHOLD) for a in sample)

    def _make_pattern(self, sample):
        pass