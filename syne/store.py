# coding: utf-8

from syne.calc import limited_add
from syne.tools import avg


class Store(object):
    """
    Stores limited number of objects with weights,
    removes objects with low weight when store is full.
    """
    def __init__(self, objects, weights, max_size, min_weight=-1000, max_weight=1000):
        """
        normalized: when False do normalizing in init
        """
        self._objects = objects
        self._weights = weights
        self._max_size = max_size
        self._min_weight = min_weight
        self._max_weight = max_weight
        self._avg_weight = (min_weight + max_weight) / 2.0

        self._compact()
        self.normalize()

    def get_objects(self):
        return self._objects

    def get_weights(self):
        return self._weights

    def increase(self, index):
        self._weights[index] += 1

    def normalize(self):
        if not self._objects:
            return

        if max(self._weights) > self._max_weight:
            self._descrease_all()

        while avg(self._weights) > self._avg_weight:
            self._descrease_all()

    def add(self, obj):
        self._objects.append(obj)
        self._weights.append(0)
        self._compact()

    def remove(self, index):
        self._objects.pop(index)
        self._weights.pop(index)

    def _compact(self):
        while len(self._objects) > self._max_size:
            min_weight = min(self._weights)
            to_remove_index = self._weights.index(min_weight)
            self.remove(to_remove_index)

    def _descrease_all(self):
        self._weights = [
            limited_add(w, -1, self._min_weight, self._max_weight)
            for w in self._weights
        ]
