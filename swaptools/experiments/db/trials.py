
from swap.db.db import Collection, Cursor

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
            'trial': dict,
            'golds': dict,
            'thresholds': list,
        }

    def _init_collection(self):
        pass

    #######################################################################

    def add(self, trial):
        data = trial.dict()
        self.insert(data)

    def get(self, trial_id):
        pass
