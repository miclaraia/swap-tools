
import swap.config as config

from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class UserBurnin(Experiment):

    @classmethod
    def new(cls, gamma, num_golds, *args, **kwargs):
        e = super().new(*args, **kwargs)

        gamma._name('gamma')
        num_golds._name('golds')

        e.values = VI(gamma, num_golds)
        return e

    def setup_next(self):
        info = self.trial_info

        if self.values['gamma'].first():
            self.gg.random(info['golds'])

        config.gamma = info['gamma']

    def _plot(self, p):
        p.plot_2d('info.gamma', 'score_stats.purity')
        p.plot_2d('info.gamma', 'score_stats.completeness')
        p.plot_2d('info.gamma', 'score_stats.retired')
        p.plot_2d('info.gamma', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('info.gamma', 'score_stats.tnr')
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
            kwargs['num_golds'] = VI.single(golds)

        if args.gamma:
            a = [int(i) for i in args.gamma[:3]]
            kwargs['gamma'] = VI.range(*a)

        e = UserBurnin.new(**kwargs)
        e.run()

        return e
