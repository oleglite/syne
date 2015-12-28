# -*- coding: utf-8 -*-

import struct


def bytes_to_ints(bytes):
    """
    >>> bytes_to_ints(b'\x01\x10\x02')
    (1, 16, 2)
    """
    return struct.unpack('>%sB' % len(bytes), bytes)


def ints_to_bytes(ints):
    """
    >>> list(ints_to_bytes((1, 16, 2)))
    b'\x01\x10\x02'
    """
    return struct.pack('>B', *ints)
