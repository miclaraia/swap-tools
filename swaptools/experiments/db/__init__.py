
import swaptools.experiments.config as config
from swaptools.experiments.db.experiment import Experiments
from swaptools.experiments.db.trials import Trials
from swaptools.experiments.db.plots import Plots
from swap.utils import Singleton
from pymongo import MongoClient

import atexit

import logging
logger = logging.getLogger(__name__)


class _DB:
    """
        DB

        The main interaction between the python code and the
        supporting mongo database. All calls to the database
        should be made from here.
    """

    def __init__(self):
        logger.info('opening mongo connection')

        # Get database configuration from config file
        # pylint: disable=E1101
        host = config.experiments.host
        db_name = config.experiments.name
        port = config.experiments.port

        self._client = MongoClient('%s:%d' % (host, port))
        self._db = self._client[db_name]
        self.batch_size = int(config.experiments.max_batch_size)

        self.experiments = Experiments(self)
        self.trials = Trials(self)
        self.plots = Plots(self)
        # pylint: enable=E1101

    def setBatchSize(self, size):
        self.batch_size = size

    def close(self):
        logger.info('closing mongo connection')
        self._client.close()


class DB(_DB, metaclass=Singleton):
    pass


# class Config(_Config, metaclass=Singleton):
#     pass


@atexit.register
def goodbye():
    DB().close()
