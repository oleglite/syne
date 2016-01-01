# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import argh
from syne_audio.run import run


argh.dispatch_commands([run])
