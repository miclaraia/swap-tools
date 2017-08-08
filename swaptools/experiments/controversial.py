
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class Controversial(Experiment):

    def __init__(self, experiment, name, description,
                 num_golds=None, controversial=None, consensus=None):
        super().__init__(experiment, name, description)

        if num_golds is None:
            num_golds = 5
        if controversial is None:
            controversial = (100, 200, 100)
        if consensus is None:
            consensus = (100, 200, 100)

        self.num_golds = num_golds
        self.num_cv = controversial
        self.num_cn = consensus
        self.trial_info.update({'golds': 0, 'cv': 0, 'cn': 0})

        self._golds = None

    @staticmethod
    def info_key_order():
        return ['n', 'golds', 'cv', 'cn']

    def has_next(self, info):
        return info['cn'] <= self.num_cn[1]

    def setup(self):
        super().setup()

        gg = self.gg
        self._golds = {
            'seed': gg.random(self.num_golds)(),
            'cv': list(gg.controversial(self.num_cv[1])()),
            'cn': list(gg.consensus(self.num_cn[1])())
        }

    def setup_first(self, info):
        super().setup_first(info)
        info['cv'] = self.num_cv[0]
        info['cn'] = self.num_cn[0]

    def setup_increment(self, info):
        super().setup_increment(info)

        info['cv'] += self.num_cv[2]
        if info['cv'] > self.num_cv[1]:
            info['cv'] = self.num_cv[0]
            info['cn'] += self.num_cn[2]

    def setup_next(self):
        super().setup_next()
        info = self.trial_info

        gg = self.gg
        gg.reset()
        gg.these(self._golds['seed'])
        gg.subjects(self._golds['cv'][:info['cv']])
        gg.subjects(self._golds['cn'][:info['cn']])

        info['golds'] = len(gg.golds)
        logger.info('using %d golds', len(gg.golds))

    def _plot(self, p):
        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d(
            'golds', 'score_stats.retired_correct',
            {'y': 'Retired Correct'})
        p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'golds',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cv', 'score_stats.purity', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.completeness', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.retired', 'info.cn')
        p.plot_3d(
            'info.cv', 'score_stats.retired_correct', 'info.cn',
            {'y': 'Retired Correct'})
        p.plot_3d('info.cv', 'score_stats.tpr', 'info.cn', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cv',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cn', 'score_stats.purity', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.completeness', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.retired', 'info.cv')
        p.plot_3d(
            'info.cn', 'score_stats.retired_correct', 'info.cv',
            {'y': 'Retired Correct'})
        p.plot_3d('info.cn', 'score_stats.tpr', 'info.cv', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cn',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next()
        s = 40
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.purity',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.completeness',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.retired',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.retired_correct',
            {'x': 'Controversial', 'y': 'Consensus', 'z': 'Retired Correct'},
            s=s)
        p.plot_3d(
            'info.cv', 'info.cn', 'golds',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)

        p.next()
        p.plot_3d(
            'score_stats.purity', 'score_stats.completeness',
            'golds')
        p.plot_3d(
            'score_stats.purity', 'score_stats.completeness',
            'info.cv')
        p.plot_3d(
            'score_stats.purity', 'score_stats.completeness',
            'info.cn')
        p.plot_3d('score_stats.purity', 'score_stats.completeness',
                  'score_stats.retired')
        p.plot_3d(
            'score_stats.retired', 'score_stats.retired_correct',
            'info.cv')
        p.plot_3d(
            'score_stats.retired', 'score_stats.retired_correct',
            'info.cn')

        p.next({'s': 40})
        p.plot_3d(
            'info.cv',
            'info.cn',
            'gold_stats.controversial.mean',
            {'c': 'Controversial Average'})
        p.plot_3d(
            'info.cv',
            'info.cn',
            'gold_stats.consensus.mean',
            {'c': 'Consensus Average'})
        p.kwargs = {}
        p.plot_2d('score_stats.fnr', 'score_stats.fpr')

        p.next()
        p.plot_3d('gold_stats.true', 'gold_stats.false', 'score_stats.purity')
        p.plot_2d('gold_stats.fraction', 'score_stats.purity')
        p.plot_2d('gold_stats.fraction', 'score_stats.completeness')
        p.plot_2d('gold_stats.fraction', 'score_stats.retired')
        p.plot_3d('info.cv', 'gold_stats.fraction', 'info.cn')
        p.plot_3d('info.cn', 'gold_stats.fraction', 'info.cv')

        p.next()
        p.plot_3d('info.cv', 'gold_stats.fraction', 'info.cn')
        p.plot_3d('info.cv', 'gold_stats.fraction', 'score_stats.purity')
        p.plot_3d('info.cv', 'gold_stats.fraction', 'score_stats.completeness')
        p.plot_3d('info.cv', 'gold_stats.fraction', 'score_stats.retired')

        p.next()
        p.plot_3d('info.cn', 'gold_stats.fraction', 'info.cv')
        p.plot_3d('info.cn', 'gold_stats.fraction', 'score_stats.purity')
        p.plot_3d('info.cn', 'gold_stats.fraction', 'score_stats.completeness')
        p.plot_3d('info.cn', 'gold_stats.fraction', 'score_stats.retired')

        p.plot_standard('golds')

        p.next()
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.purity', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.purity', 'info.cn',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.completeness', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.completeness', 'info.cn',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.retired', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.retired', 'info.cn',
            {'x': 'NCL'})
        p.run()


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
