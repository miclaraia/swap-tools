
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)

class Controversial(Experiment):

    def __init__(self, experiment, name, description):
        super().__init__(experiment, name, description)
        self._golds = None

    @classmethod
    def new(cls, num_golds, controversial, consensus, *args, **kwargs):
        e = super().new(*args, **kwargs)

        controversial._name('cv')
        consensus._name('cn')
        num_golds._name('seed')

        e.values = VI(controversial, consensus, num_golds)

        return e

    def setup(self):
        super().setup()

        info = self.trial_info
        cv = self.values['cv'].end
        cn = self.values['cn'].end
        seed = self.values['seed'].current

        gg = self.gg
        self._golds = {
            'seed': list(gg.random(seed)()),
            'cv': list(gg.controversial(cv)()),
            'cn': list(gg.consensus(cn)())
        }

    def setup_next(self):
        info = self.trial_info

        # TODO: Ensure there is no overlap between these subjects
        gg = self.gg
        gg.reset()
        gg.subjects(self._golds['seed'])
        gg.subjects(self._golds['cv'][:info['cv']])
        gg.subjects(self._golds['cn'][:info['cn']])

        info['golds'] = len(gg.golds)
        logger.info('using %d golds', len(gg.golds))

    def _plot(self, p):
        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d('golds', 'score_stats.mse_t')
        p.plot_2d('golds', 'score_stats.mse')
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'golds',
            axes={'x': 'Bogus Threshold',
                  'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cv', 'score_stats.purity', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.completeness', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.retired', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.mse_t', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.mse', 'info.cn')
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cv',
            axes={'x': 'Bogus Threshold',
                  'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cn', 'score_stats.purity', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.completeness', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.retired', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.mse_t', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.mse', 'info.cv')
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cn',
            axes={'x': 'Bogus Threshold',
                  'y': 'Real Threshold'})

        p.next()
        p.plot_ebar('info.cv', 'score_stats.mse_t')
        p.plot_ebar('info.cv', 'score_stats.mse')
        p.plot_ebar('info.cn', 'score_stats.mse_t')
        p.plot_ebar('info.cn', 'score_stats.mse')

        p.next({'s': 40})
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.purity',
            axes={'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.completeness',
            axes={'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.retired',
            axes={'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.mse_t',
            axes={'x': 'Controversial', 'y': 'Consensus'})
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.mse',
            axes={'x': 'Controversial', 'y': 'Consensus'})

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
            axes={'c': 'Controversial Average'})
        p.plot_3d(
            'info.cv',
            'info.cn',
            'gold_stats.consensus.mean',
            axes={'c': 'Consensus Average'})
        p.plot_args._reset()
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

        p.plot_3d(
            'info.fraction',
            'score_stats.retired_correct',
            'info.golds',
            ylim=(.7, 1),
        )
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
            kwargs['num_golds'] = VI.single(golds)

        if args.controversial:
            a = [int(i) for i in args.controversial[0:3]]
            kwargs['controversial'] = VI.range(*a)

        if args.consensus:
            a = [int(i) for i in args.consensus[0:3]]
            kwargs['consensus'] = VI.range(*a)

        e = Controversial.new(**kwargs)
        e.run()

        return e
