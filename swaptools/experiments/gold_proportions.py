
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import math
import logging

logger = logging.getLogger(__name__)

class GoldProportions(Experiment):

    @classmethod
    def new(cls, num_golds, fraction, series, *args, **kwargs):
        e = super().new(*args, **kwargs)

        series._name('series')
        fraction._name('fraction')
        num_golds._name('golds')

        e.values = VI(series, fraction, num_golds)

        return e

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
        p.next(None, {'discrete': False})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.fraction',
                  axes={'x': 'Bogus Threshold',
                        'y': 'Real Threshold'})

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_3d(
            'info.fraction',
            'score_stats.purity',
            'info.golds',
            ylim=(.65, .9),
        )
        p.plot_3d(
            'info.fraction',
            'score_stats.completeness',
            'info.golds',
            ylim=(0, .4),
        )
        p.plot_3d(
            'info.fraction',
            'score_stats.retired',
            'info.golds',
            ylim=(0, 1),
        )
        p.plot_3d(
            'info.fraction',
            'score_stats.retired_correct',
            'info.golds',
            ylim=(.7, 1),
        )
        p.plot_3d('info.fraction', 'score_stats.mse_t', 'info.golds')
        p.plot_3d('info.fraction', 'score_stats.mse', 'info.golds')

        def cond(value):
            def f(data_point):
                c = data_point[2]
                return abs(c - value) < 2
            return f

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_kde(
            'info.fraction',
            'score_stats.purity',
            'golds',
            filter=cond(5000),
            ylim=(.65, .9),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.purity',
            'golds',
            filter=cond(10000),
            ylim=(.65, .9),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.purity',
            'golds',
            filter=cond(20000),
            ylim=(.65, .9),
        )

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_kde(
            'info.fraction',
            'score_stats.completeness',
            'golds',
            filter=cond(5000),
            ylim=(0, .4),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.completeness',
            'golds',
            filter=cond(10000),
            ylim=(0, .4),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.completeness',
            'golds',
            filter=cond(20000),
            ylim=(0, .4),
        )

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_kde(
            'info.fraction',
            'score_stats.retired',
            'golds',
            filter=cond(5000),
            ylim=(0, 1),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.retired',
            'golds',
            filter=cond(10000),
            ylim=(0, 1),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.retired',
            'golds',
            filter=cond(20000),
            ylim=(0, 1),
        )

        p.next()
        p.plot_kde(
            'info.fraction',
            'score_stats.completeness',
            'golds',
            ylim=(0, .4),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.retired',
            'golds',
            ylim=(0, 1),
        )
        p.plot_kde(
            'info.fraction',
            'score_stats.retired_correct',
            'golds',
            ylim=(.7, 1),
        )

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_3d(
            'info.fraction', 'score_stats.mse_t', 'info.golds',
            filter=cond(20000),
            ylim=(.1, .13)
        )
        p.plot_3d(
            'info.fraction', 'score_stats.mse_t', 'info.golds',
            filter=cond(10000),
            ylim=(.1, .13)
        )
        p.plot_3d(
            'info.fraction', 'score_stats.mse_t', 'info.golds',
            filter=cond(5000),
            ylim=(.1, .13)
        )

        p.next(None, {'discrete': True, 'domain': [5000, 10000, 20000]})
        p.plot_3d(
            'info.fraction', 'score_stats.mse', 'info.golds',
            filter=cond(20000),
            ylim=(.075, .1)
        )
        p.plot_3d(
            'info.fraction', 'score_stats.mse', 'info.golds',
            filter=cond(10000),
            ylim=(.075, .1)
        )
        p.plot_3d(
            'info.fraction', 'score_stats.mse', 'info.golds',
            filter=cond(5000),
            ylim=(.075, .1)
        )

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
            kwargs['fraction'] = VI.range(*a)

        if args.series:
            series = int(args.series[0])
            kwargs['series'] = VI.range(1, series, 1)

        if args.golds:
            a = [int(i) for i in args.golds]
            kwargs['num_golds'] = VI.list(a)

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
