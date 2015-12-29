# coding: utf-8


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
