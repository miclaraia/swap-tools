
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class Controversial(Experiment):

    def __init__(self, experiment, name, description,
                 num_golds, controversial, consensus):
        super().__init__(experiment, name, description)

        self.num_golds = num_golds
        self.num_cv = controversial
        self.num_cn = consensus
        self.trial_info.update({'golds': 0, 'cv': 0, 'cn': 0})

        self._golds = None

    @staticmethod
    def info_key_order():
        return ['n', 'golds', 'cv', 'cn']

    def has_next(self):
        info = self.trial_info
        cv = info['cv'] + self.num_cv[2] <= self.num_cv[1]
        cn = info['cn'] + self.num_cn[2] <= self.num_cn[1]

        return cv or cn

    def setup(self):
        super().setup()
        info = self.trial_info
        info.update({
            'cv': self.num_cv[0],
            'cn': self.num_cn[0]
        })

        gg = self.gg
        self._golds = {
            'seed': gg.random(self.num_golds)(),
            'cv': list(gg.controversial(self.num_cv[1])()),
            'cn': list(gg.consensus(self.num_cn[1])())
        }

    def setup_next(self):
        super().setup_next()
        info = self.trial_info

        if info['cv'] >= self.num_cv[1]:
            info['cv'] = self.num_cv[0]
            info['cn'] += self.num_cn[2]
        else:
            info['cv'] += self.num_cv[2]

        logger.info('trial: %s', str(info))
        gg = self.gg
        gg.reset()
        gg.these(self._golds['seed'])
        gg.subjects(self._golds['cv'][:info['cv']])
        gg.subjects(self._golds['cn'][:info['cn']])

        logger.info('using %d golds', len(gg.golds))


class Interface(_Interface):

    _experiment = Controversial

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'cvcn'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument(
            '--num-golds', nargs=1)

        parser.add_argument(
            '--controversial', nargs=3)

        parser.add_argument(
            '--consensus', nargs=3)

    @staticmethod
    def required():
        return ['num_golds', 'controversial', 'consensus']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.num_golds:
            golds = int(args.num_golds[0])
            kwargs['num_golds'] = golds

        if args.controversial:
            cv = [int(i) for i in args.controversial[0:3]]
            kwargs['controversial'] = tuple(cv)

        if args.consensus:
            cn = [int(i) for i in args.consensus[0:3]]
            kwargs['consensus'] = tuple(cn)

        e = Controversial.new(**kwargs)
        e.run()

        return e
