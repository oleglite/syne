# coding: utf-8

from pprintpp import pformat


def avg(it):
    try:
        length = len(it)
    except TypeError:
        it = list(it)
        length = len(it)

    if length == 0:
        return 0

    return sum(it) / float(length)


def object_to_dict(obj):
    return {key: getattr(obj, key) for key in dir(obj) if not key.startswith('_')}


def dict_to_object(d):
    class obj: pass
    for key, value in d.items():
        setattr(obj, key, value)
    return obj


def from_plain_signal(plain_signal, total_length):
    """
    >>> from_plain_signal(2, 4)
    (0, 0, 1.0, 0)
    >>> from_plain_signal(0, 4)
    (1.0, 0, 0, 0)
    >>> from_plain_signal(1, 2)
    (0, 1.0)

    :param plain_signal: int index of signal where activity == 1.0
    :param total_length: length of signal
    :return: signal where one impulse equals to 1, the rest to 0
    """
    return tuple(1.0 if i == plain_signal else 0 for i in range(total_length))


def to_plain_signal(signal):
    """
    >>> to_plain_signal((0.6, 0.2, 0.8, 0.7))
    2
    >>> to_plain_signal((0.0, 0.1, 0.1))
    1
    >>> to_plain_signal((0.0, 0.0, 0.0))

    :param signal:
    :return: index of max value or None if all values is 0
    """
    max_value = max(signal)
    return signal.index(max_value) if max_value else None


class Buffer:
    """
    Helper class to store fixed amount of values

    >>> Buffer([1, 2])
    Buffer([1, 2])
    >>> Buffer([], size=3)
    Buffer([None, None, None])
    >>> Buffer([1, 2, 3], size=3)
    Buffer([1, 2, 3])
    >>> Buffer([1, 2], size=3)
    Buffer([None, 1, 2])
    >>> Buffer([1, 2, 3, 4], size=3)
    Buffer([2, 3, 4])
    """

    DEFAULT_VALUE = None

    def __init__(self, seq, size=None):
        values = list(seq)
        self._size = len(values) if size is None else size
        self._buffer = values

        while len(self._buffer) > self._size:
            self._buffer.pop(0)

        while len(self._buffer) < self._size:
            self._buffer.insert(0, self.DEFAULT_VALUE)

    def push(self, value):
        """
        :param value:
        :return:

        >>> buffer = Buffer([1, 2, 3])
        >>> buffer.push(4)
        >>> buffer
        Buffer([2, 3, 4])
        """
        self._buffer.append(value)
        self._buffer.pop(0)

    def __iter__(self):
        return iter(self._buffer)

    def __len__(self):
        return self._size

    def __repr__(self):
        return 'Buffer(%s)' % pformat(self._buffer)
