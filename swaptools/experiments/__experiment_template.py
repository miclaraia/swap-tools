

from swaptools.experiments.iterators import ValueIterator as VI
from swaptools.experiments.experiment import Experiment
from swaptools.experiments.experiment import Interace as _Interface

import logging

logger = logging.getLogger(__name__)


class SampleExperiment(Experiment):

    @classmethod
    def new(cls, value1, value2, *args, **kwargs):
        # Generate the experiment with the appropriate id
        # name, and description
        e = super().new(*args, **kwargs)

        # Set the names of the value iterators
        value1._name('value1')
        value2._name('value2')

        # Assign the value iterators instance variable
        e.values = [value1, value2]

        return e

    def setup(self):
        """
        Perform any initial setup operations
        """
        # super().setup()
        pass

    def setup_first(self):
        """
        Any operations that need to happen after initial setup
        but before the first trial, specific only to the first trial
        """
        pass

    def setup_next(self):
        """
        Prepare the next experiment environment
        """
        pass

    def has_next(self):
        """
        Check if there is another trial
        """
        pass

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
