
from swaptools.experiments.random_golds import RandomGolds
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class GoldProportions(Experiment):

    def __init__(self, experiment, name, description,
                 num_real=None, num_bogus=None, num_trials=10):
        super().__init__(experiment, name, description)

        if num_real is None:
            num_real = (1000, 2000, 1000)
        if num_bogus is None:
            num_bogus = (1000, 2000, 1000)

        self.num_real = num_real
        self.num_bogus = num_bogus
        self.num_trials = num_trials

        self.trial_info.update({'real': 0, 'bogus': 0})

    @staticmethod
    def info_key_order():
        return ['n', 'real', 'bogus']

    def has_next(self, info):
        return info['bogus'] <= self.num_bogus[1]

    def setup_first(self, info):
        super().setup_first(info)
        info['real'] = self.num_real[0]
        info['bogus'] = self.num_bogus[0]

    def setup_increment(self, info):
        super().setup_increment(info)
        if info['n'] >= self.num_trials:
            info['n'] = 0
            info['real'] += self.num_real[2]

            if info['real'] > self.num_real[1]:
                info['real'] = self.num_real[0]
                info['bogus'] += self.num_bogus[2]

    def setup_next(self):
        super().setup_next()
        info = self.trial_info

        self.gg.reset()
        self.gg.random(info['real'], 1)
        self.gg.random(info['bogus'], 0)

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
            '--num-real', nargs=3)

        parser.add_argument(
            '--num-bogus', nargs=3)

        parser.add_argument(
            '--num-trials', nargs=1)

    @staticmethod
    def required():
        return ['num_real', 'num_bogus', 'num_trials']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_real:
            real = [int(i) for i in args.num_real[0:3]]
            kwargs['num_real'] = tuple(real)

        if args.num_bogus:
            bogus = [int(i) for i in args.num_bogus[0:3]]
            kwargs['num_bogus'] = tuple(bogus)

        if args.num_trials:
            kwargs['num_trials'] = int(args.num_trials[0])

        e = GoldProportions.new(**kwargs)
        e.run()

        return e
