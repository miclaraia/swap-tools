
from swap.control import Control

from swaptools.experiments.experiment import Trial
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.random_golds import RandomGolds
from swaptools.experiments.db import DB
import swaptools.experiments.db.experiment as edb
import swaptools.experiments.db.trials as tdb
import swaptools.experiments.config as config

from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture(scope='module')
def override():
    config.experiments.name = 'testexperiments'
    DB._reset()

    patch.object(tdb.Trials, 'next_id', 0)
    patch.object(edb.Experiments, 'next_id', 0)


# pylint: disable=W0613,W0621,R0201
class TestExperiment:

    @patch('swap.config.back_update', True)
    @patch.object(
        edb.Experiments, 'insert',
        MagicMock())
    def test_setup(self, override):
        e = Experiment(None, None, None)
        e.setup()

        assert config.back_update is False
        assert isinstance(e.control, Control)

    def test_setupnext_first(self, override):
        e = Experiment(None, None, None)
        e.setup_next()

        assert e.trial_info['n'] == 0

    def test_setupnext(self, override):
        e = Experiment(None, None, None)
        e.trial_info['n'] = 1
        e.setup_next()

        assert e.trial_info['n'] == 2
