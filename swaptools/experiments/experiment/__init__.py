
from swap import Control
from swap.agents.agent import Stat
from swap.utils.scores import Score, ScoreExport
import swap.ui
import swaptools.experiments.config as config
import swaptools.experiments.db.experiment_data as dbe
import swaptools.experiments.db.plots as plotsdb

from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)


class Trial:
    def __init__(self, trial_id, golds, score_export):
        """
            consensus, controversial: settings used to run swap; number of
                consensus  controversial subjects used to make gold set
            golds: (dict) Gold standard set used during run
            roc_export: ScoreExport of swap scores
        """

        self.id = OrderedDict(trial_id)
        self.golds = golds
        self.scores = score_export

    def plot(self, cutoff):
        # return (self.consensus, self.controversial,
        #         self.purity(cutoff), self.completeness(cutoff))
        pass

    def _db_export_id(self):
        pass

    @classmethod
    def build_from_db(cls, experiment, trial_info):
        pass

    ###############################################################

    def n_golds(self):
        n = {-1: 0, 0: 0, 1: 0}
        for gold in self.golds.values():
            n[gold] += 1

        return n

    def purity(self, cutoff):
        return self.scores.purity(cutoff)

    def completeness(self, cutoff):
        return self.scores.completeness(cutoff)

    @staticmethod
    def scores_from_db(scores):
        scores = [(id_, Score(id_, gold, p)) for id_, gold, p in scores]
        scores = ScoreExport(dict(scores), new_golds=False)

        return scores

    def dict(self):
        return {
            'trial': self.id,
            'golds': self.golds,
            'score_stats': self.scores.stats.dict(),
            'gold_stats': None
        }

    # def db_export(self, name):
    #     data = []
    #     for score in self.scores.sorted_scores:
    #         item = {'experiment': name}
    #         item.update({'trial': self._db_export_id()})
    #         item.update({
    #             'subject': score.id,
    #             'gold': score.gold,
    #             'p': score.p,
    #             'used_gold': -1
    #         })
    #
    #         if score.id in self.golds:
    #             item['used_gold'] = self.golds[score.id]
    #
    #         data.append(item)
    #
    #     return data


class Experiment:
    # Make sure to override
    Trial = Trial

    def __init__(self, name, cutoff):
        self.name = name
        self.trials = []
        self.plot_points = []

        self.p_cutoff = cutoff

    ###############################################################
    # Override

    def _run(self):
        pass

    def plot(self, type_, fname):
        pass

    @classmethod
    def trial_from_db(cls, trial_info, golds, scores):
        return cls.Trial.build_from_db(trial_info, golds, scores)

    def _db_export_plot(self):
        pass

    ###############################################################

    def run(self):
        self._run()
        self.clear_mem()

    @classmethod
    def from_trial_export(cls, directory, cutoff, loader):
        files = get_trials(directory)

        e = cls(cutoff)
        for fname in files:
            logger.debug(fname)
            trials = loader(fname)
            for trial in trials:
                e.add_trial(trial, keep=False)
            e.trials = []

        return e

    @classmethod
    def build_from_db(cls, experiment_name, cutoff):
        e = cls(experiment_name, cutoff=cutoff)
        for trial_info, golds, scores in dbe.get_trials(experiment_name):

            # trial = Trial(cn, cv, golds, scores)
            trial = cls.trial_from_db(trial_info, golds, scores)
            e.add_trial(trial, keep=False)

        return e

    @classmethod
    def init_swap(cls):
        control = Control()
        control.run()

        return control.getSWAP()

    def clear_mem(self):
        """
            Saves trial objects to disk to free up memory
        """
        dbe.upload_trials(self.trials, self.name)
        self.trials = []

    def add_trial(self, trial, keep=True):
        if keep:
            self.trials.append(trial)
            if len(self.trials) >= config.trials.keep_amount:
                self.clear_mem()

        self.plot_points.append(trial.plot(self.p_cutoff))

    def __str__(self):
        s = '%d points\n' % len(self.plot_points)
        s += str(Stat([i[2] for i in self.plot_points]))
        return s


def get_trials(directory):
    import os
    import re

    pattern = re.compile('trials_cv_[0-9]{1,4}_cn_[0-9]{1,4}.pkl')

    def _path(fname):
        return os.path.join(directory, fname)

    def istrial(fname):
        if pattern.match(fname):
            return True
        else:
            return False

    files = []
    for fname in os.listdir(directory):
        path = _path(fname)
        if os.path.isfile(path) and istrial(fname):
            files.append(path)

    return files
