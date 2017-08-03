
from swaptools.experiments.random_golds import RandomGolds
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb

from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


def generate():
    e = RandomGolds(None, None, None, (100, 200, 100), 5)

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    return e


# pylint: disable=W0613,W0621,R0201
class TestRandomGolds:

    def test_setup_next_first(self, override):
        e = generate()
        e.setup_next()

        assert e.trial_info == {'n': 0, 'golds': 100}

    def test_setup_next(self, override):
        e = generate()
        e.setup_next()
        e.setup_next()

        assert e.trial_info == {'n': 1, 'golds': 100}

    def test_rollover(self, override):
        e = generate()
        info = {'n': 4, 'golds': 100}
        e.setup_increment(info)

        assert info == {'n': 0, 'golds': 200}

    def test_increment(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100}
        e.setup_increment(info)

        assert info == {'n': 1, 'golds': 100}

    def test_has_next_true(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100}
        e.setup_increment(info)

        assert e.has_next(info) is True

    def test_has_next_false(self, override):
        e = generate()
        info = {'n': 4, 'golds': 200}
        e.setup_increment(info)

        assert e.has_next(info) is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 10
