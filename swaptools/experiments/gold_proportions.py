
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

    def has_next(self):
        n = self.trial_info['n']
        if n is None:
            return True

        n = n + 1 <= self.num_trials - 1

        real = self.trial_info['real'] + self.num_real[2]
        real = real <= self.num_real[1]

        bogus = self.trial_info['bogus'] + self.num_bogus[2]
        bogus = bogus <= self.num_bogus[1]

        return n or real or bogus

    def setup(self):
        super().setup()
        self.trial_info['real'] = self.num_real[0]
        self.trial_info['bogus'] = self.num_bogus[0]

    def setup_next(self):
        super().setup_next()
        info = self.trial_info
        if info['n'] >= self.num_trials:
            info['n'] = 0

            if info['real'] >= self.num_real[1]:
                info['real'] = self.num_real[0]
            else:
                info['real'] += self.num_real[2]

        info['bogus'] += self.num_bogus[2]

        logger.info('%s %s', str(info), str(self.num_trials))
        self.gg.reset()
        self.gg.random(info['real'], 1)
        self.gg.random(info['bogus'], 0)

    def _plot(self, p):
        RandomGolds._plot(self, p)


class Interface(_Interface):

    _experiment = GoldProportions

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'godlprop'

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
