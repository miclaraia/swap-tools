
import swap.config as config

from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface
from swaptools.experiments.db import DB

import logging

logger = logging.getLogger(__name__)

class UserBurnin(Experiment):

    def __init__(self, experiment, name, description,
                 gamma, num_golds):
        super().__init__(experiment, name, description)

        self.gamma = gamma
        self.num_golds = num_golds
        self.trial_info.update({'gamma': 0})

    @staticmethod
    def info_key_order():
        return ['n', 'gamma']

    @classmethod
    def new(cls, *args, **kwargs):
        kwargs['experiment'] = DB().experiments.next_id()
        return cls(*args, **kwargs)

    def has_next(self):
        gamma = self.trial_info['gamma']
        return gamma + self.gamma[2] <= self.gamma[1]

    def setup(self):
        super().setup()
        self.trial_info['gamma'] = self.gamma[0] - self.gamma[2]
        self.gg.random(self.num_golds)

    def setup_next(self):
        super().setup_next()
        info = self.trial_info
        info['gamma'] += self.gamma[2]

        logger.info('Gamma %d', info['gamma'])
        config.gamma = info['gamma']


class Interface(_Interface):

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
            '--num-golds', nargs=1, required=True)

        parser.add_argument(
            '--gamma', nargs=3, required=True)

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
