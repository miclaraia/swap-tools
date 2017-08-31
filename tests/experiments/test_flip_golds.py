
from swaptools.experiments.flip_golds import FlipGolds
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from swaptools.experiments.iterators import ValueIterator

from unittest.mock import patch, MagicMock
import pytest
from collections import OrderedDict


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)

def gen_golds(n):
    out = {}
    for k in range(n):
        if k < n / 2:
            v = 0
        else:
            v = 1
        out[k] = v
    return out


def generate():
    kwargs = {
        'name': None, 'description': None,
        'golds': ValueIterator.list([50, 100, 200]),
        'fraction_flipped': ValueIterator.range(.2, .8, .2),
        'series': ValueIterator.range(1, 3, 1)
    }
    e = FlipGolds.new(**kwargs)

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    return e


# pylint: disable=W0613,W0621,R0201
class TestRandomGolds:

    def test_setup_next_first(self, override):
        e = generate()
        e._setup_next()

        assert e.trial_info == {
            'n': 0,
            'series': 1,
            'flipped': .2,
            'golds': 50
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'series': 1,
            'flipped': .4,
            'golds': 50
        }

    def test_rollover_1(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 1
        e.values['flipped'].current = .8
        e.values['golds'].current = 50

        e._setup_next()

        assert e.trial_info == {
            'n': 5,
            'series': 2,
            'flipped': .2,
            'golds': 50
        }

    def test_rollover_2(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 3
        e.values['flipped'].current = .8
        e.values['golds'].current = 50

        e._setup_next()

        assert e.trial_info == {
            'n': 5,
            'series': 1,
            'flipped': .2,
            'golds': 100
        }

    def test_has_next_true(self, override):
        e = generate()
        e.n = 4
        e.values['flipped'].current = .8
        e.values['golds'].current = 100

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 3
        e.values['flipped'].current = .8
        e.values['golds'].current = 200

        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 36

    def test_flip_golds_1(self):
        golds = gen_golds(10)
        g = FlipGolds.flip_golds(golds, .5)
        assert g == {k: 1 for k in range(10)}

    def test_flip_golds_2(self):
        golds = gen_golds(10)
        g = FlipGolds.flip_golds(golds, .25)
        assert g == {
            0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1
        }

    def test_flip_golds_3(self):
        golds = gen_golds(10)
        g = FlipGolds.flip_golds(golds, .75)
        assert g == {
            0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1, 9: 1
        }

    def test_set_golds(self, override):
        e = generate()

        def f(n):
            def g():
                return {k: 1 for k in range(10)}
            return g
        e.gg.random = f
        e.setup_next()


        g = {k: 1 for k in range(10)}
        g[0] = 0
        g[1] = 0
        e.gg.these.assert_called_with(g)
