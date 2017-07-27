
from swap.db.db import Collection, Cursor

from collections import OrderedDict
from pymongo import IndexModel, ASCENDING
import logging

logger = logging.getLogger(__name__)

class Trials(Collection):

    #######################################################################

    @staticmethod
    def _collection_name():
        return 'trials'

    @staticmethod
    def _schema():
        return {
            'experiment': {'type': int},
            'trial': {'type': int},
            'info': {'type': OrderedDict},
            'golds': {'type': list},
            'thresholds': {'type': list},
            'score_stats': {'type': OrderedDict},
            'gold_stats': {'type': OrderedDict},
        }

    def _init_collection(self):
        indexes = [
            IndexModel([('experiment', ASCENDING)]),
            IndexModel([('trial', ASCENDING)]),
            IndexModel([('info', ASCENDING)])
        ]

        logger.debug('inserting %d indexes', len(indexes))
        self.collection.create_indexes(indexes)
        logger.debug('done')

    #######################################################################

    def add(self, trial):
        logger.info('adding trial %d', trial['trial'])
        data = trial.dict()
        self.insert(data)

    def get(self, trial_id):
        logger.info('getting trial %d', trial_id)
        cursor = self.collection.find({'trial': trial_id})

        if cursor.hasNext():
            return cursor.next()

    def get_trials(self, experiment_id):
        logger.info('getting trials for experiment %d', experiment_id)
        cursor = self.collection.find({'experiment': experiment_id})

        trials = []
        for data in cursor:
            trials.append(data)

        return trials

    def next_id(self):
        cursor = self.collection.find().sort('trial', -1).limit(1)

        try:
            return cursor.next()['trial'] + 1
        except StopIteration:
            return 0
