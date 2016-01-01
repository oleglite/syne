# -*- coding: utf-8 -*-

import pickle

from syne import TimeUnit, make_conf
from syne.tools import from_plain_signal, object_to_dict
from syne_audio import conf


full_conf = make_conf(conf)
unit = TimeUnit(full_conf)


def run():
    with open('output', 'rb') as f:
        data = pickle.load(f)

    frames = data['audio']['frames']
    for i, byte in enumerate(frames):
        output = unit.activate(from_plain_signal(byte, total_length=256))

        if i % 100 == 0:
            print('%d:\t %s%%' % (i, (i * 100 / len(frames))))

    data = {
        'conf': object_to_dict(full_conf),
        'unit': unit.get_data()
    }

    with open('run_unit', 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    run()
