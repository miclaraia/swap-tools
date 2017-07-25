
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
            'experiment': int,
            'trial': int,
            'info': dict,
            'golds': list,
            'score_stats': dict,
            'gold_stats': dict,
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

    def get_experiment(self, experiment_id):
        cursor = self.collection.find({'experiment': experiment_id})
        return cursor
