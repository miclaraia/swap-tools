
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

from collections import OrderedDict
import logging
import math

logger = logging.getLogger(__name__)


class FlipGolds(Experiment):

    def __init__(self, experiment, name, description):
        super().__init__(experiment, name, description)
        self.golds = {}

    @classmethod
    def new(cls, golds, fraction_flipped, *args, **kwargs):
        # Generate the experiment with the appropriate id
        # name, and description
        e = super().new(*args, **kwargs)

        # Set the names of the value iterators
        golds._name('golds')
        fraction_flipped._name('flipped')

        # Assign the value iterators instance variable
        e.values = VI(fraction_flipped, golds)

        return e

    def setup_next(self):
        """
        Prepare the next experiment environment
        """
        info = self.trial_info

        if self.values['flipped'].first():
            self.golds = OrderedDict(self.gg.random(info['golds'])())

        self.gg.reset()
        f = info['flipped']
        golds = self.flip_golds(self.golds, f)
        self.gg.these(golds)

    @staticmethod
    def flip_golds(golds, fraction):
        golds = golds.copy()

        def flip(subject):
            g = golds[subject]
            if g == 0:
                golds[subject] = 1
            if g == 1:
                golds[subject] = 0

        n = len(golds)
        n = math.floor(n * fraction)

        subjects = list(golds.keys())
        for s in subjects[:n]:
            flip(s)

        return golds

    def _plot(self, p):
        """
        Plotting for this experiment
        """


class Interface(_Interface):

    _experiment = FlipGolds

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'flipgolds'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

        parser.add_argument('--flipped', nargs=3)

        parser.add_argument('--golds', nargs='*')

        parser.add_argument('--filter-golds', nargs=1)

    @staticmethod
    def required():
        return ['flipped', 'golds']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.a:
            a = [float(i) for i in args.a[:3]]
            kwargs['a'] = VI.range(*a)

        e = FlipGolds.new(**kwargs)
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
