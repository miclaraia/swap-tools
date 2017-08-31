
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class RandomGolds(Experiment):

    @classmethod
    def new(cls, num_golds, series, *args, **kwargs):
        e = super().new(*args, **kwargs)

        series._name('series')
        num_golds._name('golds')

        e.values = VI(series, num_golds)

        return e

    def setup_next(self):
        info = self.trial_info

        self.gg.reset()
        self.gg.random(info['golds'])

    def _plot(self, p):
        p.plot_ebar('golds', 'score_stats.purity')
        p.plot_ebar('golds', 'score_stats.completeness')
        p.plot_ebar('golds', 'score_stats.retired')
        p.plot_ebar('golds', 'score_stats.mse_t')
        p.plot_ebar('golds', 'score_stats.mse')
        p.plot_3d('thresholds.0', 'thresholds.1', 'golds',
                  axes={'x': 'Bogus Threshold',
                        'y': 'Real Threshold'})

        p.next()
        p.plot_3d('golds', 'score_stats.purity', 'score_stats.completeness')
        p.plot_3d('golds', 'score_stats.purity', 'score_stats.retired')
        p.plot_3d('golds', 'score_stats.purity', 'score_stats.retired_correct')
        p.plot_3d('golds', 'score_stats.completeness', 'score_stats.purity')

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
        p.plot_3d(
            'golds', 'score_stats.ncl_mean', 'score_stats.purity',
            {'y': 'NCL'})
        p.run()


class Interface(_Interface):

    _experiment = RandomGolds

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'randomex'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument(
            '--num-golds', nargs=3)

        parser.add_argument(
            '--num-trials', nargs=1)

    @staticmethod
    def required():
        return ['num_golds', 'num_trials']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            a = [int(i) for i in args.num_golds[0:3]]
            kwargs['num_golds'] = VI.range(*a)

        if args.num_trials:
            series = int(args.num_trials[0])
            kwargs['series'] = VI.range(1, series, 1)

        e = RandomGolds.new(**kwargs)
        e.run()

        return e
