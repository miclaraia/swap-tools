
from swap import Control
from swap.utils.golds import GoldStats, GoldGetter
import swap.ui.ui as ui

import swaptools.experiments.config as config
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.db import DB
from swaptools.experiments.plots import Plotter

from collections import OrderedDict
import code
import logging
logger = logging.getLogger(__name__)


class Trial:
    def __init__(self, experiment, trial, info, golds,
                 thresholds, score_stats, gold_stats):
        """

        """

        self.id = trial
        self.experiment = experiment
        self.info = info

        self.golds = list(golds)

        self.thresholds = tuple(thresholds)
        self.score_stats = score_stats
        self.gold_stats = gold_stats

    ###############################################################

    @classmethod
    def generate(cls, experiment, trial, info, golds, score_export):
        score_stats = score_export.stats.dict()
        thresholds = score_export.thresholds
        gold_stats = GoldStats(golds).dict()

        return cls(experiment, trial, info, list(golds),
                   thresholds, score_stats, gold_stats)

    @classmethod
    def from_db(cls, trial_data):
        keys = ['experiment', 'trial', 'info', 'golds',
                'thresholds', 'score_stats', 'gold_stats']
        kwargs = {k: trial_data[k] for k in keys}

        return cls(**kwargs)

    def dict(self):
        return OrderedDict([
            ('experiment', self.experiment),
            ('trial', self.id),
            ('info', self.info),
            ('golds', self.golds),
            ('thresholds', list(self.thresholds)),
            ('score_stats', self.score_stats),
            ('gold_stats', self.gold_stats)
        ])

    def upload(self):
        logger.debug('Uploading trial')
        DB().trials.insert(self.dict())

    @classmethod
    def interact_from_db(cls, trial_id):
        golds = DB().trials.get(trial_id)['golds']
        control = Control()
        control.gold_getter.subjects(golds)
        control.run()

        gg = GoldGetter()
        gg.subjects(golds)
        gs = GoldStats(gg.golds)

        swap = control.getSWAP()
        scores = swap.score_export()
        assert scores
        assert gs
        code.interact(local=locals())

    ###############################################################

    def __str__(self):
        d = self.dict()
        d['golds'] = len(d['golds'])
        return str(d)

    def __repr__(self):
        return str(self)


class Experiment:

    def __init__(self, experiment, name, description):
        self.id = experiment
        self.info = {
            'name': name,
            'description': description,
            'trial_id': None,
            'count': None
        }

        self._trials = {}
        # self.trial_info = OrderedDict([('n', None)])
        self.n = None

        self.control = None
        self.gg = GoldGetter()

        self.values = VI()

    ###############################################################
    ## Override by Experiment subclasses

    def setup(self):
        logger.info('Setting up')
        config.back_update = False
        self.control = self._init_control()

        count = self.count(new=True)
        logger.info('Expecting to run %d trials', count)

        # Save experiment data to database
        self.upload()

    def setup_next(self):
        pass

    def has_next(self):
        for v in self.values:
            print(v.name, v.current)
            if v.more():
                return True
        return False

    def setup_first(self):
        pass

    def setup_increment(self):
        for v in self.values:
            if v.more():
                v.step()
                break
            else:
                v.reset()

    def _plot(self, p):
        pass

    @staticmethod
    def _init_control():
        return Control()

    ###############################################################
    ## Running the experiment

    def _run(self):
        logger.info('Running trial')
        logger.debug('Using %d golds', len(self.gg.golds))
        logger.debug('gold labels: %s', str(list(self.gg.golds)))
        control = self.control
        control.reset()
        control.gold_getter.these(self.gg.golds)

        control.run()

    def _has_next(self):
        if self.n is None:
            return True

        return self.has_next()

    def _setup_next(self):
        logger.info('Setting up next trial')

        if self.n is None:
            self.n = 0
            self.setup_first()
        else:
            self.n += 1
            self.setup_increment()

        logger.info('Trial: %s', str(self.trial_info))
        self.setup_next()

    def _post(self):
        logger.info('Done running trial')
        thresholds = self.thresholds
        scores = self.control.swap.score_export(thresholds)

        trial = Trial.generate(
            experiment=self.id, trial=self.info['trial_id'],
            info=self.trial_info,
            golds=self.gg.golds, score_export=scores)

        self.add_trial(trial)
        self.info['trial_id'] += 1

        return trial

    def run(self):
        self.setup()
        while self._has_next():
            self._setup_next()
            self._run()
            self._post()

        self.clean_db()
        logger.info('All done, experiment %d, trials %d',
                    self.id, len(self._trials))

    def plot(self, fname):
        self._add_fraction_stat()

        plotter = Plotter(self, fname)
        self._plot(plotter)

    def _add_fraction_stat(self):
        for trial in self.trials:
            g = trial.gold_stats
            g['fraction'] = g['true'] / g['total']

    ###############################################################

    @classmethod
    def from_db(cls, experiment_id):
        data = DB().experiments.get(experiment_id)
        kwargs = {
            'experiment': data['experiment'],
            'name': data['name'],
            'description': data['description']
        }

        experiment = cls(**kwargs)
        experiment._fetch_trials()
        return experiment

    @classmethod
    def new(cls, *args, **kwargs):
        kwargs['experiment'] = DB().experiments.next_id()
        return cls(*args, **kwargs)

    ###############################################################

    @property
    def thresholds(self):
        history = self.control.swap.history
        thresholds = history.score_export().thresholds
        logger.info('Using thresholds %s', str(thresholds))

        return thresholds

    @property
    def trials(self):
        for trial in self._trials.values():
            yield trial

    @property
    def trial_info(self):
        values = [(v.name, v.current) for v in self.values]
        return OrderedDict([('n', self.n)] + values)

    def count(self, new=False):
        if new or self.info['count'] is None:
            c = 1
            for v in self.values:
                c *= v.count()
            self.info['count'] = c

        return self.info['count']

    def dict(self):
        name = self.info['name']
        desc = self.info['description']
        return OrderedDict([
            ('experiment', self.id),
            ('name', name),
            ('description', desc),
            ('trials', self.count())
        ])

    def add_trial(self, trial):
        logger.info('adding trial %s', trial)
        self._trials[trial.id] = trial
        trial.upload()

    def _fetch_trials(self):
        data = DB().trials.get_trials(self.id)

        trials = {}
        for trial in data:
            if 'score_stats' in trial and 'purity' in trial['score_stats']:
                trial = Trial.from_db(trial)
                trials[trial.id] = trial

        self._trials = trials
        return trials

    def upload(self):
        logger.info('Uploading experiment')
        DB().experiments.insert(self.dict())
        trial_id = DB().trials.reserve(self.id, self.count())

        self.info['trial_id'] = trial_id

    def clean_db(self):
        DB().trials.reserve_clear(self.id)


class Interace(ui.Interface):
    """
    Interface that defines a set of options and operations.
    Designed to be subclassed and overriden
    """

    _experiment = Experiment

    def options(self, parser):
        """
        Add options to the parser
        """
        parser.add_argument(
            '--run', action='store_true')

        parser.add_argument(
            '--shell', action='store_true')

        parser.add_argument(
            '--interact', nargs=1
        )

        parser.add_argument(
            '--plot', nargs=2,
            metavar=('experiment', 'fname'),
            help='Plot experiment stored in db'
        )

        parser.add_argument('--name', nargs=1)
        parser.add_argument('--description', nargs=1)

    def required(self):
        pass

    def run(self, name, description, args):
        pass

    @staticmethod
    def _required(required, args):
        args = args.__dict__
        for r in required:
            if not args[r]:
                print(r)
                raise Exception

    def call(self, args):
        """
        Define what to do if this interface's command was passed
        """
        experiment = None
        if args.run:
            r = ['name', 'description'] + self.required()
            self._required(r, args)

            name = args.name[0]
            desc = args.description[0]
            experiment = self.run(name, desc, args)

        if args.interact:
            trial_id = int(args.interact[0])
            Trial.interact_from_db(trial_id)

        if args.plot:
            e = self._plot_make_e(args)
            self.plot(args, e)

        if args.shell:
            assert experiment
            code.interact(local=locals())

    def _plot_make_e(self, args):
        experiment_id = int(args.plot[0])
        e = self._experiment.from_db(experiment_id)
        return e

    def plot(self, args, experiment):
        fname = self.f(args.plot[1])
        experiment.plot(fname)
