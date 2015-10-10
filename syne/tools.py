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

