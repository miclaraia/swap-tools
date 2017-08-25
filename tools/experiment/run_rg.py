#!/usr/bin/env python

from swap import config
import swap.config.logger

from swaptools.experiments.random_golds import RandomGolds
from swaptools.experiments.iterators import ValueIterator as VI

from os import path

def override_config():
    here = path.abspath(path.dirname(__file__))
    fname = path.join(here, 'experiment_config.py')
    config.import_config(fname)
    swap.config.logger.init()

def main():
    override_config()

    golds = list(range(1000, 10001, 1000))
    golds += [15000, 10000]
    kwargs = {
        'name': 'randomex-5',
        'description': 'Run randomex experiment with MSE and MSE_T calculation',
        'num_golds': VI.list(golds),
        'series': VI.range(1, 20, 1),
    }
    e = RandomGolds.new(**kwargs)
    e.run()
    return e


if __name__ == '__main__':
    main()
