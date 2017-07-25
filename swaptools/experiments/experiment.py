
from swap import Control
from swap.utils.stats import Stat
from swap.utils.scores import Score, ScoreExport, ScoreStats
from swap.utils.golds import GoldStats, GoldGetter
import swap.ui

import swaptools.experiments.config as config
import swaptools.experiments.db.experiment_data as dbe
import swaptools.experiments.db.plots as plotsdb

from collections import OrderedDict
import code
import logging
logger = logging.getLogger(__name__)


class Trial:
    def __init__(self, experiment, trial, info, golds, score_export):
        """
            consensus, controversial: settings used to run swap; number of
                consensus  controversial subjects used to make gold set
            golds: (dict) Gold standard set used during run
            roc_export: ScoreExport of swap scores
        """

        self.id = trial
        self.experiment = experiment
        self.info = info

        self.golds = list(golds)

        self.score_stats = score_export.stats.dict()
        self.gold_stats = GoldStats(golds).dict()

    def plot(self, cutoff):
        # return (self.consensus, self.controversial,
        #         self.purity(cutoff), self.completeness(cutoff))
        pass

    def _db_export_id(self):
        pass

    ###############################################################

    def dict(self):
        return {
            'experiment': self.experiment,
            'trial': self.id,
            'info': self.info,
            'golds': self.golds,
            'score_stats': self.score_stats,
            'gold_stats': self.gold_stats,
        }

    @classmethod
    def interact_from_db(cls, trial_data):
        control = Control()
        control.gold_getter.subjects(trial_data['golds'])
        control.run()

        code.interact(local=locals())


class Experiment:

    def __init__(self, description):
        pass

    def _run(self):
        pass

    def run(self):
        pass

    def export_trials(self):
        pass
