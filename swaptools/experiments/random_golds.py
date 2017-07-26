
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface
from swaptools.experiments.db import DB

import logging

logger = logging.getLogger(__name__)

class RandomGolds(Experiment):

    def __init__(self, experiment, name, description,
                 num_golds=None, num_trials=10):
        super().__init__(experiment, name, description)

        if num_golds is None:
            num_golds = (1000, 2000, 1000)

        self.num_golds = num_golds
        self.num_trials = num_trials

        self.trial_info.update({'golds': 0})

    @classmethod
    def new(cls, *args, **kwargs):
        kwargs['experiment'] = DB().experiments.next_id()
        return cls(*args, **kwargs)

    def has_next(self):
        n = self.trial_info['n']
        if n is None:
            return True
        n += 1

        golds = self.trial_info['golds']
        golds += self.num_golds[2]

        if n >= self.num_trials and golds > self.num_golds[1]:
            return False
        return True

    def setup(self):
        super().setup()
        self.trial_info['golds'] = self.num_golds[0]

    def setup_next(self):
        super().setup_next()
        info = self.trial_info
        if info['n'] >= self.num_trials:
            self.trial_info['n'] = 0
            info['golds'] += self.num_golds[2]

        logger.info('%s %s', str(info), str(self.num_trials))
        self.gg.reset()
        self.gg.random(info['golds'])


class Interface(_Interface):

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
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            golds = [int(i) for i in args.num_golds[0:3]]
            kwargs['num_golds'] = tuple(golds)

        if args.num_trials:
            kwargs['num_trials'] = int(args.num_trials[0])

        e = RandomGolds.new(**kwargs)
        e.run()

        return e
