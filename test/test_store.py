# coding: utf-8

from syne.store import Store


def test_add():
    store = Store([], [], 5, min_weight=-10, max_weight=10)

    store.add(1)
    assert store.get_objects() == [1]
    assert store.get_weights() == [0]

    obj = {1: 2}
    store.add(obj)
    assert store.get_objects() == [1, obj]
    assert store.get_weights() == [0, 0]


def test_add_to_full_store():
    store = Store([1, 2, 3], [-1, -2, 1], 3, min_weight=-10, max_weight=10)

    store.add(4)
    assert store.get_objects() == [1, 3, 4]
    assert store.get_weights() == [-1, 1, 0]


def test_add_to_full_store_remove_oldest():
    store = Store([1, 2, 3], [0, 0, 0], 3, min_weight=-10, max_weight=10)

    store.add(4)
    assert store.get_objects() == [2, 3, 4]
    assert store.get_weights() == [0, 0, 0]


def test_increase():
    store = Store([1, 2, 3], [10, -10, -10], 3, min_weight=-10, max_weight=10)

    store.increase(0)
    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [11, -10, -10]

    store.increase(2)
    store.increase(2)
    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [11, -10, -8]


def test_normalize_by_average():
    store = Store([1, 2, 3], [1, 2, 3], 3, min_weight=-10, max_weight=10)

    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [-1, 0, 1]

    store.increase(0)
    store.normalize()
    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [-1, -1, 0]


def test_normalize_by_max():
    store = Store([1, 2, 3], [-10, -2, 10], 3, min_weight=-10, max_weight=10)

    store.normalize()
    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [-10, -2, 10]     # nothing changed

    store.increase(2)
    # wight of 3 now is 11
    store.normalize()
    # 1 - already min weight
    # 2 - decreased because decreasing all
    # 3 - decreased from 11 to 10
    assert store.get_objects() == [1, 2, 3]
    assert store.get_weights() == [-10, -3, 10]
