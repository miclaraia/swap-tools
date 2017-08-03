
import swap.config as config

from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class UserBurnin(Experiment):

    def __init__(self, experiment, name, description,
                 gamma=None, num_golds=None):
        super().__init__(experiment, name, description)

        if gamma is None:
            gamma = (1, 5, 1)
        if num_golds is None:
            num_golds = 1000

        self.gamma = gamma
        self.num_golds = num_golds
        self.trial_info.update({'gamma': 0})

    @staticmethod
    def info_key_order():
        return ['n', 'gamma']

    def has_next(self, info):
        return info['gamma'] <= self.gamma[1]

    def setup(self):
        super().setup()
        self.gg.random(self.num_golds)

    def setup_first(self, info):
        super().setup_first(info)
        info['gamma'] = self.gamma[0]

    def setup_increment(self, info):
        super().setup_increment(info)
        info['gamma'] += self.gamma[2]

    def setup_next(self):
        super().setup_next()
        info = self.trial_info

        config.gamma = info['gamma']

    def _plot(self, p):
        p.plot_2d('info.gamma', 'score_stats.purity')
        p.plot_2d('info.gamma', 'score_stats.completeness')
        p.plot_2d('info.gamma', 'score_stats.retired')
        p.plot_2d('info.gamma', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d(
            'info.gamma', 'score_stats.ncl_mean',
            {'y': 'NCL'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.gamma',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})
        p.next()

        p.plot_3d('score_stats.purity', 'score_stats.completeness',
                  'info.gamma')
        p.plot_3d('score_stats.purity', 'score_stats.completeness',
                  'score_stats.retired')
        p.plot_2d('score_stats.fnr', 'score_stats.fpr')
        p.plot_3d('score_stats.retired', 'score_stats.retired_correct',
                  'score_stats.purity')
        p.next()
        p.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.retired',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.retired_correct',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.gamma',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})
        p.next()

        p.plot_standard('info.gamma')

        p.run()

        # p.next()
        # p.plot_3d('gold_stats.controversial.mean', 'info.gamma', 'score_stats.retired',
        #           {'x': 'Controversial'})
        # p.plot_3d('score_stats.purity', 'score_stats.completeness',
        #           'info.gamma')
        # p.plot_3d('score_stats.purity', 'score_stats.completeness',
        #           'score_stats.retired')
        # p.plot_2d('score_stats.mdr', 'score_stats.fpr')
        #
        # p.next()
        # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
        #           'score_stats.purity',
        #           {'x': 'Controversial', 'y': 'Consensus'})
        # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
        #           'score_stats.completeness',
        #           {'x': 'Controversial', 'y': 'Consensus'})
        # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
        #           'score_stats.retired',
        #           {'x': 'Controversial', 'y': 'Consensus'})
        # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
        #           'info.gamma',
        #           {'x': 'Controversial', 'y': 'Consensus'})
        # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
        #           'score_stats.ncl_mean',
        #           {'x': 'Controversial', 'y': 'Consensus', 'c': 'NCL'})
        #
        # p.next()
        # p.plot_2d('score_stats.ncl_mean','score_stats.retired_correct',
        #           {'x': 'NCL',
        #            'c': 'Retired Correct'})
        # p.plot_2d('info.gamma', 'score_stats.retired_correct', {'c': 'Retired Correct'})
        # p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.retired_correct',
        #           {'x': 'NCL',
        #            'c': 'Retired Correct'})
        # p.plot_3d('score_stats.ncl_mean', 'score_stats.retired_correct', 'info.gamma',
        #           {'x': 'NCL',
        #            'y': 'Retired Correct'})
        #
        # p.next()
        # p.plot_2d('score_stats.ncl_mean', 'score_stats.retired',
        #           {'x': 'NCL'})
        # p.plot_2d('info.gamma', 'score_stats.retired')
        # p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.retired',
        #           {'x': 'NCL'})
        # p.plot_3d('score_stats.ncl_mean', 'score_stats.retired', 'info.gamma',
        #           {'x': 'NCL'})
        #
        # p.next()
        # p.plot_2d('score_stats.ncl_mean', 'score_stats.purity',
        #           {'x': 'NCL'})
        # p.plot_2d('info.gamma', 'score_stats.purity')
        # p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.purity',
        #           {'x': 'NCL'})
        # p.plot_3d('score_stats.ncl_mean', 'score_stats.purity', 'info.gamma',
        #           {'x': 'NCL'})
        #
        # p.next()
        # p.plot_2d('score_stats.ncl_mean', 'score_stats.completeness',
        #           {'x': 'NCL'})
        # p.plot_2d('info.gamma', 'score_stats.completeness')
        # p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.completeness',
        #           {'x': 'NCL'})
        # p.plot_3d('score_stats.ncl_mean', 'score_stats.completeness', 'info.gamma',
        #           {'x': 'NCL'})
        # p.run()


class Interface(_Interface):

    _experiment = UserBurnin

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'burnin'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument(
            '--num-golds', nargs=1)

        parser.add_argument(
            '--gamma', nargs=3)

    @staticmethod
    def required():
        return ['num_golds', 'gamma']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            golds = int(args.num_golds[0])
            kwargs['num_golds'] = golds

        if args.gamma:
            gamma = [int(i) for i in args.gamma[0:3]]
            kwargs['gamma'] = tuple(gamma)

        e = UserBurnin.new(**kwargs)
        e.run()

        return e
