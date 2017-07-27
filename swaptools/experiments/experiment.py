
from swap import Control
from swap.utils.golds import GoldStats, GoldGetter
import swap.ui.ui as ui

import swaptools.experiments.config as config
from swaptools.experiments.db import DB

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

    def plot(self):
        pass

    ###############################################################

    @classmethod
    def generate(cls, experiment, trial, info, golds, score_export):
        score_stats = score_export.stats.dict()
        thresholds = score_export.thresholds
        gold_stats = GoldStats(golds).dict()

        return cls(experiment, trial, info, list(golds),
                   thresholds, score_stats, gold_stats)

    @classmethod
    def from_db(cls, trial_id):
        data = DB().trials.get(trial_id)
        keys = ['experiment', 'trial', 'info', 'golds',
                'thresholds', 'score_stats', ' gold_stats']
        kwargs = {k: data[k] for k in keys}

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

    @classmethod
    def interact_from_db(cls, trial_id):
        golds = DB().trials.get(trial_id)['golds']
        control = Control()
        control.gold_getter.subjects(golds)
        control.run()

        swap = control.getSWAP()
        scores = swap.score_export()
        assert scores
        code.interact(local=locals())

    ###############################################################

    def __str__(self):
        return str(self.dict())

    def __repr__(self):
        return str(self)


class Experiment:

    def __init__(self, experiment, name, description):
        self.id = experiment
        self.name = name
        self.description = description

        self._trials = {}
        self.trial_info = OrderedDict([('n', None)])
        self.trial_id = None

        self.control = None
        self.gg = GoldGetter()

    ###############################################################

    def setup(self):
        logger.info('Setting up')
        config.back_update = False
        self.control = self._init_control()

    @property
    def thresholds(self):
        history = self.control.swap.history
        thresholds = history.score_export().thresholds
        logger.info('Using thresholds %s', str(thresholds))

        return thresholds

    @staticmethod
    def has_next():
        return False

    def setup_next(self):
        logger.info('Setting up next trial')
        if self.trial_info['n'] is None:
            self.trial_info['n'] = 0
        else:
            self.trial_info['n'] += 1

    def _run(self):
        logger.info('Running trial')
        logger.debug('Using %d golds', len(self.gg.golds))
        control = self.control
        control.reset()
        control.gold_getter.these(self.gg.golds)

        control.run()

    def post(self):
        logger.info('Done running trial')
        thresholds = self.thresholds
        scores = self.control.swap.score_export(thresholds)

        if self.trial_id is None:
            self.trial_id = DB().trials.next_id()
        else:
            self.trial_id += 1

        trial = Trial.generate(
            experiment=self.id, trial=self.trial_id,
            info=self.trial_info.copy(),
            golds=self.gg.golds, score_export=scores)
        self.add_trial(trial)

        return trial

    def run(self):
        self.setup()
        while self.has_next():
            self.setup_next()
            self._run()
            self.post()
        logger.info('Done running trials')
        self.upload()
        logger.info('All done, experiment %d, trials %d',
                    self.id, len(self._trials))

    ###############################################################

    @staticmethod
    def _init_control():
        return Control()

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
        experiment.fetch_trials()
        return experiment

    @classmethod
    def generate(cls, name, description):
        experiment = DB().experiments.next_id()
        return cls(experiment, name, description)

    @property
    def trials(self):
        for trial in self._trials.values():
            yield trial

    def dict(self):
        return {
            'experiment': self.id,
            'name': self.name,
            'description': self.description
        }

    def add_trial(self, trial):
        logger.info('adding trial %s', trial)
        self._trials[trial.id] = trial

    def fetch_trials(self):
        data = DB().trials.get_trials(self.id)

        trials = {}
        for trial in data:
            trial = Trial.from_db(trial)
            trials[trial.id] = trial

        self._trials = trials
        return trials

    def upload(self):
        logger.info('Uploading trials')
        DB().experiments.insert(self.dict())

        trials = []
        for trial in self.trials:
            trials.append(trial.dict())
        print(trials)
        DB().trials.insert_many(trials)


class Interace(ui.Interface):
    """
    Interface that defines a set of options and operations.
    Designed to be subclassed and overriden
    """

    def options(self, parser):
        """
        Add options to the parser
        """
        parser.add_argument(
            '--run', action='store_true')

        parser.add_argument(
            '--shell', action='store_true')

        parser.add_argument('name', nargs=1)
        parser.add_argument('description', nargs=1)

    def run(self, name, description, args):
        pass

    def call(self, args):
        """
        Define what to do if this interface's command was passed
        """
        experiment = None
        if args.run:
            name = args.name[0]
            desc = args.description[0]
            experiment = self.run(name, desc, args)

        if args.shell:
            assert experiment
            code.interact(local=locals())
