
from swaptools.experiments.random_golds import RandomGolds
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
    golds = ValueIterator.range(100, 200, 100)
    series = ValueIterator.range(1, 5, 1)
    kwargs = {'name': None, 'description': None}

    e = RandomGolds.new(golds, series, **kwargs)

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
            'golds': 100
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'series': 2,
            'golds': 100
        }

    def test_rollover(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 5
        e.values['golds'].current = 100

        e._setup_next()

        assert e.trial_info == {
            'n': 5,
            'series': 1,
            'golds': 200
        }

    def test_has_next_true(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 5
        e.values['golds'].current = 100

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()
        e.n = 4
        e.values['series'].current = 5
        e.values['golds'].current = 200

        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 10
