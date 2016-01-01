from syne.time_unit import TimeUnit
from syne.space_unit import SpaceUnit
from syne import conf as default_conf
from syne.tools import dict_to_object, object_to_dict


__all__ = (
    'TimeUnit',
    'SpaceUnit',
    'make_conf'
)


def make_conf(*args, **kwargs):
    """
    1. get_conf(conf_module)
    2. get_conf(key=value, ...)

    :return: conf with default values added (where needed)
    """
    conf = object_to_dict(default_conf)

    if len(args) == 1:
        dict_conf = object_to_dict(args[0])
    else:
        dict_conf = kwargs

    conf.update(dict_conf)
    return dict_to_object(conf)
