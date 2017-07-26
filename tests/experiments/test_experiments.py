
from swap.control import Control

from swaptools.experiments.experiment import Trial
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.random_golds import RandomGolds
import swaptools.experiments.config as config

from unittest.mock import MagicMock, patch


class TestTrial:

    pass


class TestExperiment:

    @patch('swap.config.back_update', True)
    def test_setup(self):
        e = Experiment(None, None, None)
        e.setup()

        assert config.back_update is False
        assert isinstance(e.control, Control)

    def test_setupnext_first(self):
        e = Experiment(None, None, None)
        e.setup_next()

        assert e.trial_info['n'] == 0

    def test_setupnext(self):
        e = Experiment(None, None, None)
        e.trial_info['n'] = 1
        e.setup_next()

        assert e.trial_info['n'] == 2


class TestRandomex:

    def test_setupnext_middle(self):
        e = RandomGolds(None, None, None, (1, 5, 1), 4)
        e.trial_info = {'n': 2, 'golds': 2}

        e.setup_next()
        assert e.trial_info['n'] == 3
        assert e.trial_info['golds'] == 2

    def test_setupnext_rollover(self):
        e = RandomGolds(None, None, None, (1, 5, 1), 4)
        e.trial_info = {'n': 3, 'golds': 2}

        e.setup_next()
        assert e.trial_info['n'] == 0
        assert e.trial_info['golds'] == 3

    def test_hasnext_true(self):
        e = RandomGolds(None, None, None, (1, 5, 1), 4)
        e.trial_info = {'n': 3, 'golds': 2}

        assert e.has_next() is True

    def test_hasnext_false(self):
        e = RandomGolds(None, None, None, (1, 5, 1), 4)
        e.trial_info = {'n': 3, 'golds': 5}

        assert e.has_next() is False
