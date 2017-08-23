
from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

from collections OrderedDict
import logging

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

    def setup(self):
        """
        Perform any initial setup operations
        """
        # super().setup()
        pass

    def setup_next(self):
        """
        Prepare the next experiment environment
        """
        info = self.trial_info

        if self.values['flipped'].first():
            self.golds = OrderedDict(self.gg.random(info['golds'])())

        def flip(golds, fraction):
            

        self.gg.reset()
        golds = v{}
        self.gg.these()


    def _plot(self, p):
        """
        Plotting for this experiment
        """


class Interface(_Interface):

    _experiment = SampleExperiment

    @property
    def command(self):
        """
        Command used to select parser.

        For example, this would return 'swap' for SWAPInterface
        and 'roc' for RocInterface
        """
        return 'sample'

    def options(self, parser):
        """
        Add options to the parser
        """
        super().options(parser)

    @staticmethod
    def required():
        return ['a', 'b', 'c']

    @staticmethod
    def run(name, description, args):
        kwargs = {
            'name': name,
            'description': description,
        }
        if args.a:
            a = [float(i) for i in args.a[:3]]
            kwargs['a'] = VI.range(*a)

        e = SampleExperiment.new(**kwargs)
        e.run()

        return e
