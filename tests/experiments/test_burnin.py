
from swaptools.experiments.user_burnin import UserBurnin
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from swaptools.experiments.iterators import ValueIterator as VI

from unittest.mock import patch
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


def generate():
    gamma = VI.range(1, 5, 1)
    golds = VI.single(1000)
    kwargs = {'name': None, 'description': None}

    return UserBurnin.new(gamma, golds, **kwargs)


# pylint: disable=W0613,W0621,R0201
class TestBurnin:

    def test_setup_next_first(self, override):
        e = generate()
        e._setup_next()

        assert e.trial_info == {
            'n': 0,
            'gamma': 1,
            'golds': 1000
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'gamma': 2,
            'golds': 1000
        }

    def test_has_next_true(self, override):
        e = generate()
        e.n = 1
        e.values['gamma'].current = 2

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()
        e.n = 1
        e.values['gamma'].current = 5

        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 5
