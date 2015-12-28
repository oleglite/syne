# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import argh
import pickle

from syne import Unit, get_conf
from syne_audio import conf


def run():
    unit = Unit(get_conf(conf))

    with open('output', 'rb') as f:
        data = pickle.load(f)
        import pdb; pdb.set_trace()


argh.dispatch_commands([run])
