# -*- coding: utf-8 -*-

import pickle

from syne import TimeUnit, make_conf
from syne.tools import from_plain_signal, object_to_dict, dict_to_object
from syne_audio import conf as audio_conf


FILENAME = '../output'


def teach_unit(unit):
    with open(FILENAME, 'rb') as f:
        data = pickle.load(f)

    frames = data['audio']['frames']
    for i, byte in enumerate(frames):
        output = unit.activate(from_plain_signal(byte, total_length=256))

        if i % 100 == 0:
            print('%d:\t %s%%' % (i, (i * 100 / len(frames))))

        if i > 10000:
            return


def save_unit(unit, path):
    data = {
        'conf': object_to_dict(unit.conf),
        'unit': unit.get_data()
    }

    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load_unit(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)

    conf = make_conf(dict_to_object(data['conf']))
    unit = TimeUnit(conf, data=data['unit'])
    return unit


def run():
    conf = make_conf(audio_conf)
    unit = TimeUnit(conf)
    teach_unit(unit)


if __name__ == '__main__':
    run()
