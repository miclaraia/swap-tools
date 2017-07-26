
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
            'name': str,
            'description': str
        }

    def _init_collection(self):
        pass

    #######################################################################

    def add(self, experiment):
        data = experiment.dict()
        self.insert(data)

    def get(self, experiment_id):
        cursor = self.collection.find({'experiment': experiment_id})

        if cursor.hasNext():
            return cursor.next()

    def next_id(self):
        cursor = self.collection.find().sort({'experiment': -1}).limit(1)

        if cursor.hasNext():
            return cursor.next()['experiment'] + 1

        return 0
