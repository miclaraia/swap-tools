
import swap.config as config

from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class Prior(Experiment):

    def __init__(self, experiment, name, description,
                 prior=None, num_golds=None, num_trials=None):
        super().__init__(experiment, name, description)

        if prior is None:
            prior = (.05, .95, .05)
        if num_golds is None:
            num_golds = 5000
        if num_trials is None:
            num_trials = 3

        self.prior = prior
        self.num_golds = num_golds
        self.num_trials = num_trials
        self.trial_info.update({
            'prior': None, 'golds': None, 'series': None})

    @staticmethod
    def info_key_order():
        return ['n', 'series', 'prior', 'golds']

    def has_next(self, info):
        return info['series'] < self.num_trials

    def setup(self):
        super().setup()
        self.gg.random(self.num_golds)

    def setup_first(self, info):
        super().setup_first(info)
        info['prior'] = self.prior[0]
        info['golds'] = self.num_golds
        info['series'] = 0

    def setup_increment(self, info):
        super().setup_increment(info)
        info['prior'] += self.prior[2]

        if info['prior'] > self.prior[1]:
            info['prior'] = self.prior[0]
            info['series'] += 1

    def setup_next(self):
        series = self.trial_info['series']

        super().setup_next()
        info = self.trial_info

        if info['series'] != series:
            gg = self.gg
            gg.reset()
            gg.random(info['golds'])

        config.p0 = info['prior']

    def _plot(self, p):
        p.plot_2d('info.prior', 'score_stats.purity')
        p.plot_2d('info.prior', 'score_stats.completeness')
        p.plot_2d('info.prior', 'score_stats.retired')
        p.plot_2d('info.prior', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('info.prior', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.prior',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('gold_stats.controversial.mean', 'golds',
                  'score_stats.retired',
                  {'x': 'Controversial'})
        p.plot_3d('score_stats.purity', 'score_stats.completeness',
                  'golds')
        p.plot_3d('score_stats.purity', 'score_stats.completeness',
                  'score_stats.retired')
        p.plot_2d('score_stats.fnr', 'score_stats.fpr')
        p.plot_3d('score_stats.retired', 'score_stats.retired_correct',
                  'score_stats.purity')

        p.next()
        p.plot_3d('gold_stats.true', 'gold_stats.false', 'score_stats.purity')
        p.plot_3d('gold_stats.fraction', 'score_stats.purity', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.completeness', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.retired', 'golds')

        p.plot_standard('golds')

        p.next()
        p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
                  'score_stats.purity',
                  {'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
                  'score_stats.completeness',
                  {'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
                  'score_stats.retired',
                  {'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
                  'golds',
                  {'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
                  'score_stats.ncl_mean',
                  {'x': 'Controversial', 'y': 'Consensus', 'c': 'NCL'})

        p.next()
        p.plot_3d('score_stats.ncl_mean', 'score_stats.purity', 'golds',
                  {'x': 'NCL'})
        p.plot_3d('score_stats.ncl_mean', 'score_stats.completeness', 'golds',
                  {'x': 'NCL'})
        p.plot_3d('score_stats.ncl_mean', 'score_stats.retired_correct',
                  'golds',
                  {'x': 'NCL',
                   'y': 'Retired Correct'})
        p.plot_3d('score_stats.ncl_mean', 'score_stats.retired', 'golds',
                  {'x': 'NCL'})
        p.plot_2d(
            'golds', 'score_stats.ncl_mean',
            {'y': 'NCL'})
        p.run()


class Interface(_Interface):

    _experiment = Prior

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'prior'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument(
            '--num-golds', nargs=1)

        parser.add_argument(
            '--prior', nargs=3)

        parser.add_argument(
            '--num-trials', nargs=1
        )

    @staticmethod
    def required():
        return ['num_golds', 'prior', 'num_trials']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            golds = int(args.num_golds[0])
            kwargs['num_golds'] = golds

        if args.prior:
            prior = [float(i) for i in args.prior[0:3]]
            kwargs['prior'] = tuple(prior)

        if args.num_trials:
            kwargs['num_trials'] = int(args.num_trials[0])

        e = Prior.new(**kwargs)
        e.run()

        return e
