
from swaptools.experiments.prior import Prior
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
    e = Prior(None, None, None, (.2, .8, .2), 100, 3)

    gg = MagicMock()
    gg.golds = {i: i for i in range(200)}

    e.gg = gg

    return e


# pylint: disable=W0613,W0621,R0201
class TestPrior:

    def test_setup_first(self, override):
        e = generate()
        e.setup_next()

        assert e.trial_info == {'n': 0, 'golds': 100, 'prior': .2, 'series': 0}

    def test_setup_next(self, override):
        e = generate()
        e.setup_next()
        e.setup_next()

        assert e.trial_info == {'n': 1, 'golds': 100, 'prior': .4, 'series': 0}

    def test_rollover(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100, 'prior': .8, 'series': 0}
        e.setup_increment(info)

        assert info == {'n': 1, 'golds': 100, 'prior': .2, 'series': 1}

    def test_increment(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100, 'prior': .4, 'series': 0}
        e.setup_increment(info)

        compare = {'n': 1, 'golds': 100, 'prior': .6, 'series': 0}
        print(compare)
        print(info)
        for k, v in compare.items():
            print(k, v)
            if type(v) is float:
                assert info[k] - v < 1e-6
            else:
                assert info[k] == v

    def test_has_next_true(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100, 'prior': .4, 'series': 0}
        e.setup_increment(info)

        assert e.has_next(info) is True

    def test_has_next_false(self, override):
        e = generate()
        info = {'n': 0, 'golds': 100, 'prior': .8, 'series': 2}
        e.setup_increment(info)

        assert e.has_next(info) is False

    def test_count(self, override):
        e = generate()
        assert e.count() == 12
