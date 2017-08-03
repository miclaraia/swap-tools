
from swap.db.db import Collection, Schema

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
            'experiment': {'type': int},
            'name': {'type': str},
            'description': {'type': str},
            'trials': {'type': int},
        }

    def _init_collection(self):
        pass

    #######################################################################

    def get(self, experiment_id):
        cursor = self.collection.find({'experiment': experiment_id})

        if cursor.count() > 0:
            return cursor.next()

    def next_id(self):
        cursor = self.collection.find().sort('experiment', -1).limit(1)

        if cursor.count() == 0:
            return 0
        return cursor.next()['experiment'] + 1
