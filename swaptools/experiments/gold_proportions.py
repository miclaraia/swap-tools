
from swaptools.experiments.iterators import ValueIterator
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import math
import logging

logger = logging.getLogger(__name__)

class GoldProportions(Experiment):

    def __init__(self, experiment, name, description,
                 num_golds=None, fraction=None, series=None):
        super().__init__(experiment, name, description)

        if num_golds and fraction and series:
            series._name('series')
            fraction._name('fraction')
            num_golds._name('golds')

        self.values = [series, fraction, num_golds]

    def setup_next(self):
        info = self.trial_info

        g = info['golds']
        f = info['fraction']

        real = math.floor(g * f)
        bogus = math.ceil(g * (1 - f))

        self.gg.reset()
        self.gg.random(real, 1)
        self.gg.random(bogus, 0)

    def _plot(self, p):
        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d('golds', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'golds',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('info.real', 'score_stats.purity', 'info.bogus')
        p.plot_3d('info.real', 'score_stats.completeness', 'info.bogus')
        p.plot_3d('info.real', 'score_stats.retired', 'info.bogus')
        p.plot_3d('info.real', 'score_stats.retired_correct', 'info.bogus',
                  {'y': 'Retired Correct'})
        p.plot_3d('info.real', 'score_stats.tpr', 'info.bogus', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.real',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('info.bogus', 'score_stats.purity', 'info.real')
        p.plot_3d('info.bogus', 'score_stats.completeness', 'info.real')
        p.plot_3d('info.bogus', 'score_stats.retired', 'info.real')
        p.plot_3d('info.bogus', 'score_stats.retired_correct', 'info.real',
                  {'y': 'Retired Correct'})
        p.plot_3d('info.bogus', 'score_stats.tpr', 'info.real', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.bogus',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('gold_stats.true', 'gold_stats.false', 'score_stats.purity')
        p.plot_3d('gold_stats.fraction', 'score_stats.purity', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.completeness', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.retired', 'golds')

        p.plot_standard('golds')

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
        p.plot_3d('info.real', 'gold_stats.controversial.mean',
                  'gold_stats.consensus.mean',
                  {'y': 'Controversial', 'c': 'Consensus'})
        p.plot_3d('info.real', 'gold_stats.consensus.mean',
                  'gold_stats.controversial.mean',
                  {'y': 'Consensus', 'c': 'Controversial'})
        p.plot_3d('info.bogus', 'gold_stats.controversial.mean',
                  'gold_stats.consensus.mean',
                  {'y': 'Controversial', 'c': 'Consensus'})
        p.plot_3d('info.bogus', 'gold_stats.consensus.mean',
                  'gold_stats.controversial.mean',
                  {'y': 'Consensus', 'c': 'Controversial'})

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

    _experiment = GoldProportions

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'goldprop'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument(
            '--fraction', nargs=3)

        parser.add_argument(
            '--series', nargs=1)

        parser.add_argument(
            '--golds', nargs='*')

        parser.add_argument(
            '--filter-golds', nargs=1
        )

    @staticmethod
    def required():
        return ['fraction', 'series', 'golds']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.fraction:
            a = [float(i) for i in args.fraction[:3]]
            kwargs['fraction'] = ValueIterator.range(*a)

        if args.series:
            series = int(args.series[0])
            kwargs['series'] = ValueIterator.range(1, series, 1)

        if args.golds:
            a = [int(i) for i in args.golds]
            kwargs['num_golds'] = ValueIterator.list(a)

        e = GoldProportions.new(**kwargs)
        e.run()

        return e

    def plot(self, args, experiment):
        if args.filter_golds:
            r = []
            golds = int(args.filter_golds[0])
            for t in experiment.trials:
                if len(t.golds) != golds:
                    r.append(t.id)

            for i in r:
                experiment._trials.pop(i)

        super().plot(args, experiment)
