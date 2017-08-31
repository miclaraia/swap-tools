
import swap.config as config

from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class Prior(Experiment):

    @classmethod
    def new(cls, prior, num_golds, series, *args, **kwargs):
        e = super().new(*args, **kwargs)

        prior._name('prior')
        num_golds._name('golds')
        series._name('series')

        e.values = VI(prior, series, num_golds)

        return e

    def setup_next(self):
        info = self.trial_info

        if info['prior'].first():
            self.gg.reset()
            self.gg.random(info['golds'])

        config.p0 = info['prior']

    def _plot(self, p):
        p.next(None, {'discrete': True})
        p.plot_3d('info.prior', 'score_stats.purity', 'info.series')
        p.plot_3d('info.prior', 'score_stats.completeness', 'info.series')
        p.plot_3d('info.prior', 'score_stats.retired', 'info.series')
        p.plot_2d('info.prior', 'score_stats.mse_t')
        p.plot_2d('info.prior', 'score_stats.mse')
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.prior',
                  axes={'x': 'Bogus Threshold',
                        'y': 'Real Threshold'},
                  discrete=False,
        )

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
            '--series', nargs=1
        )

    @staticmethod
    def required():
        return ['num_golds', 'prior', 'series']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            a = int(args.num_golds[0])
            kwargs['num_golds'] = VI.single(a)

        if args.prior:
            a = [float(i) for i in args.prior[0:3]]
            kwargs['prior'] = VI.range(*a)

        if args.series:
            series = int(args.series[0])
            kwargs['series'] = VI.range(1, series, 1)

        e = Prior.new(**kwargs)
        e.run()

        return e
