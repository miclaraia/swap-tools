
from swap.db.db import Collection

import logging

logger = logging.getLogger(__name__)

class Experiments(Collection):

    #######################################################################

    @staticmethod
    def _collection_name():
        return 'experiments'

    @staticmethod
    def _schema():
        return {
            'experiment': int,
            'description': str
        }

    def _init_collection(self):
        pass

    #######################################################################

    def add(self, experiment):
        data = experiment.dict()
        self.insert(data)

    def get(self, trial_id):
        cursor = self.collection.find({'experiment': trial_id})

        if cursor.hasNext():
            return cursor.next()
