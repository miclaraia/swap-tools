
from swap.db.db import Collection, Cursor

from collections import OrderedDict
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
            'info': {'type': dict},
            'golds': {'type': list},
            'thresholds': {'type': list},
            'score_stats': {'type': dict},
            'gold_stats': {'type': dict},
        }

    def _init_collection(self):
        pass

    #######################################################################

    def add(self, trial):
        data = trial.dict()
        self.insert(data)

    def get(self, trial_id):
        cursor = self.collection.find({'trial': trial_id})

        if cursor.hasNext():
            return cursor.next()

    def get_trials(self, experiment_id):
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
