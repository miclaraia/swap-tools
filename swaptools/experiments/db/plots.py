
from swap.db.db import Collection, Cursor

from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

class Plots(Collection):

    #######################################################################

    @staticmethod
    def _collection_name():
        return 'plots'

    @staticmethod
    def _schema():
        return {
            'plot': {'type': int},
            'name': {'type': str},
            'type': {'type': str},
            'points': {'type': list},
            'axes': {'type': dict}
        }

    def _init_collection(self):
        pass

    #######################################################################

    def add(self, data):
        logger.info('adding plot')
        self.insert(data)

    def get(self, plot, use_name=False):
        if use_name:
            cursor = self.collection.find({'name': plot})
        else:
            cursor = self.collection.find({'plot': plot})

        if cursor.count() > 0:
            plot = cursor.next()
            plot.pop('_id')
            return plot

    def next_id(self):
        cursor = self.collection.find().sort('plot', -1).limit(1)

        if cursor.count() == 0:
            return 0
        return cursor.next()['plot'] + 1
