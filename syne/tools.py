# coding: utf-8


def avg(it):
    try:
        length = len(it)
    except TypeError:
        it = list(it)
        length = len(it)
    return sum(it) / length

