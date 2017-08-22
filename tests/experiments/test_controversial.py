
from swaptools.experiments.controversial import Controversial
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
    cv = ValueIterator.range(100, 200, 100)
    cn = ValueIterator.range(100, 200, 100)
    golds = ValueIterator.range(100, 100, 1)
    kwargs = {'name': None, 'description': None}

    e = Controversial.new(golds, cv, cn, **kwargs)

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
        e._setup_next()

        assert e.trial_info == {
            'n': 0,
            'cv': 100,
            'cn': 100,
            'seed': 100
        }

    def test_setup_next(self, override):
        e = generate()
        e._setup_next()
        e._setup_next()

        assert e.trial_info == {
            'n': 1,
            'cv': 200,
            'cn': 100,
            'seed': 100
        }

    def test_rollover(self, override):
        e = generate()
        e.n = 4
        e.values[0].current = 200
        e.values[1].current = 100

        e._setup_next()

        assert e.trial_info == {
            'n': 5,
            'cv': 100,
            'cn': 200,
            'seed': 100
        }

    def test_has_next_true(self, override):
        e = generate()
        e.n = 4
        e.values[0].current = 200
        e.values[1].current = 100

        assert e.has_next() is True

    def test_has_next_false(self, override):
        e = generate()
        e.n = 4
        e.values[0].current = 200
        e.values[1].current = 200

        assert e.has_next() is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 4
