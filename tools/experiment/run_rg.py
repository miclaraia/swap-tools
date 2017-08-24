#!/usr/bin/env python


from swaptools.experiments.random_golds import RandomGolds
from swaptools.experiments.iterators import ValueIterator as VI

def main():
    golds = list(range(1000, 10001, 1000))
    golds += [15000, 10000]
    kwargs = {
        'name': 'randomex-4',
        'description': 'Run randomex experiment with MSE and MSE_T calculation',
        'num_golds': VI.list(golds),
        'series': VI.range(1, 20, 1),
    }
    e = RandomGolds.new(**kwargs)
    e.run()
    return e


if __name__ == '__main__':
    main()
