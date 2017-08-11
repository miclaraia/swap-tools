#!/usr/bin/env python
from swaptools.experiments.random_golds import RandomGolds
from swaptools.experiments.user_burnin import UserBurnin
from swaptools.experiments.controversial import Controversial
from swaptools.experiments.gold_proportions import GoldProportions
from swaptools.experiments.prior import Prior
from swaptools.experiments.plots import Plotter

class Plot:

    def __init__(self):
        self.plotters = []

    @staticmethod
    def get_experiment(i, e_type, fname):

        e = e_type.from_db(i)
        e.add_fraction_stat()
        plotter = Plotter(e, fname)
        return plotter


    def plot(self):
        for p in self.plotters:
            p.run()

    def add(self, plotter):
        self.plotters.append(plotter)


# pylint: disable=E1120
def main():
    plotter = Plot()

    # Generate prior experiment plots
    def prior():
        p = Plot.get_experiment(6, Prior, '1-prior-%d.png')
        p.plot_2d('info.prior', 'score_stats.purity')
        p.plot_2d('info.prior', 'score_stats.completeness')
        p.plot_2d('info.prior', 'score_stats.retired')
        p.plot_2d('info.prior', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('info.prior', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.prior',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.run()
    prior()

    def rg():
        p = Plot.get_experiment(8, RandomGolds, '2-rg-%d.png')
        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d('golds', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'golds',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'golds')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'golds')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'golds')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'golds')

        p.run()
    rg()

    def gamma():
        p = Plot.get_experiment(10, UserBurnin, '3-gamma-%d.png')

        p.plot_2d('info.gamma', 'score_stats.purity')
        p.plot_2d('info.gamma', 'score_stats.completeness')
        p.plot_2d('info.gamma', 'score_stats.retired')
        p.plot_2d('info.gamma', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('info.gamma', 'score_stats.tnr')
        p.plot_3d('thresholds.0', 'thresholds.1', 'info.gamma',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})
        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'info.gamma')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'info.gamma')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'info.gamma')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'info.gamma')

        p.run()
    gamma()

    def fraction():
        p = Plot.get_experiment(9, GoldProportions, '4-gp-%d.png')

        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d('golds', 'score_stats.retired_correct',
                  {'y': 'Retired Correct'})
        p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d('thresholds.0', 'thresholds.1', 'golds',
                  {'x': 'Bogus Threshold',
                   'y': 'Real Threshold'})

        p.next()
        p.plot_3d('info.real', 'score_stats.purity', 'info.bogus')
        p.plot_3d('info.real', 'score_stats.completeness', 'info.bogus')
        p.plot_3d('info.real', 'score_stats.retired', 'info.bogus')
        p.plot_3d('info.bogus', 'score_stats.purity', 'info.real')
        p.plot_3d('info.bogus', 'score_stats.completeness', 'info.real')
        p.plot_3d('info.bogus', 'score_stats.retired', 'info.real')

        p.next()
        p.plot_3d('gold_stats.true', 'gold_stats.false', 'score_stats.purity')
        p.plot_3d('gold_stats.fraction', 'score_stats.purity', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.completeness', 'golds')
        p.plot_3d('gold_stats.fraction', 'score_stats.retired', 'golds')

        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'info.real')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'info.real')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'info.real')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'info.real')


        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'info.bogus')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'info.bogus')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'info.bogus')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'info.bogus')


        p.run()
    fraction()

    def cvcn():
        p = Plot.get_experiment(7, Controversial, '5-cvcn-%d.png')
        p.plot_2d('golds', 'score_stats.purity')
        p.plot_2d('golds', 'score_stats.completeness')
        p.plot_2d('golds', 'score_stats.retired')
        p.plot_2d(
            'golds', 'score_stats.retired_correct',
            {'y': 'Retired Correct'})
        p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'golds',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cv', 'score_stats.purity', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.completeness', 'info.cn')
        p.plot_3d('info.cv', 'score_stats.retired', 'info.cn')
        p.plot_3d(
            'info.cv', 'score_stats.retired_correct', 'info.cn',
            {'y': 'Retired Correct'})
        p.plot_3d('info.cv', 'score_stats.tpr', 'info.cn', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cv',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next({'s': 15, 'alpha': .5})
        p.plot_3d('info.cn', 'score_stats.purity', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.completeness', 'info.cv')
        p.plot_3d('info.cn', 'score_stats.retired', 'info.cv')
        p.plot_3d(
            'info.cn', 'score_stats.retired_correct', 'info.cv',
            {'y': 'Retired Correct'})
        p.plot_3d('info.cn', 'score_stats.tpr', 'info.cv', {'y': 'TPR'})
        p.plot_3d(
            'thresholds.0', 'thresholds.1', 'info.cn',
            {'x': 'Bogus Threshold',
             'y': 'Real Threshold'})

        p.next()
        s = 40
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.purity',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.completeness',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.retired',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)
        p.plot_3d(
            'info.cv', 'info.cn',
            'score_stats.retired_correct',
            {'x': 'Controversial', 'y': 'Consensus', 'z': 'Retired Correct'},
            s=s)
        p.plot_3d(
            'info.cv', 'info.cn', 'golds',
            {'x': 'Controversial', 'y': 'Consensus'}, s=s)


        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'info.cv')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'info.cv')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'info.cv')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'info.cv')

        p.next()
        p.plot_3d('score_stats.fnr', 'score_stats.fpr', 'info.cn')
        p.plot_3d('score_stats.tpr', 'score_stats.tnr', 'info.cn')
        p.plot_3d('score_stats.tpr', 'score_stats.fnr', 'info.cn')
        p.plot_3d('score_stats.tnr', 'score_stats.fpr', 'info.cn')

        p.next()
        p.plot_3d(
            'gold_stats.controversial.mean', 'gold_stats.consensus.mean',
            'gold_stats.fraction',
            {'x': 'Controversial', 'y': 'Consensus'}
        )
        p.plot_3d(
            'gold_stats.controversial.mean', 'gold_stats.consensus.mean',
            'gold_stats.true',
            {'x': 'Controversial', 'y': 'Consensus'}
        )
        p.plot_3d(
            'gold_stats.controversial.mean', 'gold_stats.consensus.mean',
            'gold_stats.false',
            {'x': 'Controversial', 'y': 'Consensus'}
        )

        p.next()
        p.plot_2d('gold_stats.fraction', 'score_stats.purity')
        p.plot_2d('gold_stats.fraction', 'score_stats.completeness')
        p.plot_2d('gold_stats.fraction', 'score_stats.retired')
        p.plot_3d('info.cv', 'gold_stats.fraction', 'info.cn')
        p.plot_3d('info.cn', 'gold_stats.fraction', 'info.cv')

        p.next()
        p.plot_3d(
            'info.cv', 'score_stats.ncl_mean', 'score_stats.purity'
        )
        p.plot_3d(
            'info.cv', 'score_stats.ncl_mean', 'score_stats.completeness'
        )
        p.plot_3d(
            'info.cv', 'score_stats.ncl_mean', 'score_stats.retired'
        )
        p.plot_3d(
            'info.cn', 'score_stats.ncl_mean', 'score_stats.purity'
        )
        p.plot_3d(
            'info.cn', 'score_stats.ncl_mean', 'score_stats.completeness'
        )
        p.plot_3d(
            'info.cn', 'score_stats.ncl_mean', 'score_stats.retired'
        )

        p.next()
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.purity', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.purity', 'info.cn',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.completeness', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.completeness', 'info.cn',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.retired', 'info.cv',
            {'x': 'NCL'})
        p.plot_3d(
            'score_stats.ncl_mean', 'score_stats.retired', 'info.cn',
            {'x': 'NCL'})

        p.run()
    cvcn()


    plotter.plot()


if __name__ == '__main__':
    main()
