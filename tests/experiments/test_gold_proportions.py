
from swaptools.experiments.gold_proportions import GoldProportions
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from swaptools.experiments.iterators import ValueIterator

from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


def generate():
    golds = ValueIterator.list([50, 100, 200])
    fraction = ValueIterator.range(.05, .95, .05)
    series = ValueIterator.range(1, 3, 1)
    kwargs = {'name': None, 'description': None}
    e = GoldProportions.new(golds, fraction, series, **kwargs)

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    return e


# pylint: disable=W0613,W0621,R0201
class TestGoldProportions:

    def test_setup_next_first(self, override):
        e = generate()
        e._setup_next()

        assert e.trial_info == {
            'n': 0,
            'series': 1,
            'fraction': .05,
            'golds': 50
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'series': 2,
            'fraction': .05,
            'golds': 50
        }

    def test_rollover_1(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 3
        e.values['fraction'].current = .05
        e.values['golds'].current = 50

        e._setup_next()

        print(e.trial_info)
        assert e.trial_info == {
            'n': 5,
            'series': 1,
            'fraction': .10,
            'golds': 50
        }

    def test_rollover_2(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 3
        e.values['fraction'].current = .95
        e.values['golds'].current = 100

        e._setup_next()

        print(e.trial_info)
        assert e.trial_info == {
            'n': 5,
            'series': 1,
            'fraction': .05,
            'golds': 200
        }

    def test_has_next_true(self, override):
        e = generate()

        e.n = 4
        e.values['series'].current = 3
        e.values['fraction'].current = .90
        e.values['golds'].current = 200

        print(e.values['fraction'].more())

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()

        e.n = 4
        e.values['series'].current = 3
        e.values['fraction'].current = .95
        e.values['golds'].current = 200
        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 162
