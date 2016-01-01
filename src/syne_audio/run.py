# -*- coding: utf-8 -*-

import pickle

from syne import TimeUnit, make_conf
from syne.tools import from_plain_signal
from syne_audio import conf


unit = TimeUnit(make_conf(conf))


def run():
    with open('output', 'rb') as f:
        data = pickle.load(f)

    frames = data['audio']['frames']
    for i, byte in enumerate(frames):
        output = unit.activate(from_plain_signal(byte, total_length=256))

        if i % 100 == 0:
            print('%d:\t %s%%' % (i, (i * 100 / len(frames))))



if __name__ == '__main__':
    run()
