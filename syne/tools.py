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
