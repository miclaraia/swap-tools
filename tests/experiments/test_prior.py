
from swaptools.experiments.prior import Prior
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from swaptools.experiments.iterators import ValueIterator as VI

from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


def generate():
    prior = VI.range(.2, .8, .2)
    golds = VI.single(100)
    series = VI.range(1, 3, 1)
    kwargs = {'name': None, 'description': None}

    e = Prior.new(prior, golds, series, **kwargs)

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    return e


# pylint: disable=W0613,W0621,R0201
class TestPrior:

    def test_setup_first(self, override):
        e = generate()
        e._setup_next()

        assert e.trial_info == {
            'n': 0,
            'golds': 100,
            'prior': .2,
            'series': 1
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'golds': 100,
            'prior': .4,
            'series': 1
        }

    def test_rollover(self, override):
        e = generate()

        e.n = 4
        e.values['prior'].current = .8
        e._setup_next()

        assert e.trial_info == {
            'n': 5,
            'golds': 100,
            'prior': .2,
            'series': 2
        }

    def test_has_next_true(self, override):
        e = generate()

        e.n = 4
        e.values['prior'].current = .8
        e.values['series'].current = 2

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()

        e.n = 4
        e.values['prior'].current = .8
        e.values['series'].current = 3

        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 12
