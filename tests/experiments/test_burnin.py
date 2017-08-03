
from swaptools.experiments.user_burnin import UserBurnin
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from unittest.mock import patch
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


def generate():
    return UserBurnin(None, None, None, (1, 5, 1), 1000)


# pylint: disable=W0613,W0621,R0201
class TestBurnin:

    def test_setup_next_first(self, override):
        e = generate()
        e.setup_next()

        assert e.trial_info == {'n': 0, 'gamma': 1}

    def test_setup_next(self, override):
        e = generate()
        e.setup_next()
        e.setup_next()

        assert e.trial_info == {'n': 1, 'gamma': 2}

    def test_increment(self, override):
        e = generate()
        info = {'n': 1, 'gamma': 2}
        e.setup_increment(info)

        assert info == {'n': 2, 'gamma': 3}

    def test_has_next_true(self, override):
        e = generate()
        info = {'n': 1, 'gamma': 2}
        e.setup_increment(info)

        assert e.has_next(info) is True

    def test_has_next_false(self, override):
        e = generate()
        info = {'n': 5, 'gamma': 5}
        e.setup_increment(info)

        assert e.has_next(info) is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 5
