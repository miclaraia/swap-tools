
from swaptools.experiments.controversial import Controversial
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
    e = Controversial(
        None, None, None,
        1000, (100, 200, 100), (100, 200, 100))

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    e._golds = {
        'seed': range(1000, 2000),
        'cv': range(200),
        'cn': range(500, 700)
    }

    return e


# pylint: disable=W0613,W0621,R0201
class TestControversial:

    def test_setup_next_first(self, override):
        e = generate()
        e.setup_next()

        assert e.trial_info == {'n': 0, 'cv': 100, 'cn': 100, 'golds': 200}

    def test_setup_next(self, override):
        e = generate()
        e.setup_next()
        e.setup_next()

        assert e.trial_info == {'n': 1, 'cv': 200, 'cn': 100, 'golds': 200}

    def test_rollover(self, override):
        e = generate()
        info = {'n': 0, 'cv': 200, 'cn': 100, 'golds': 200}
        e.setup_increment(info)

        print(info)
        assert info == {'n': 1, 'cv': 100, 'cn': 200, 'golds': 200}

    def test_increment(self, override):
        e = generate()
        info = {'n': 1, 'cv': 100, 'cn': 100, 'golds': 200}
        e.setup_increment(info)

        assert info == {'n': 2, 'cv': 200, 'cn': 100, 'golds': 200}

    def test_has_next_true(self, override):
        e = generate()
        info = {'n': 0, 'cv': 200, 'cn': 100, 'golds': 200}
        e.setup_increment(info)

        assert e.has_next(info) is True

    def test_has_next_false(self, override):
        e = generate()
        info = {'n': 0, 'cv': 200, 'cn': 200, 'golds': 200}
        e.setup_increment(info)

        assert e.has_next(info) is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 4
