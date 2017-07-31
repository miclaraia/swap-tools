
from swaptools.experiments.db import DB
from swaptools.experiments.experiment import Experiment

import numpy as np
import matplotlib.pyplot as plt


def plot(func):
    def wrapper(self, *args, **kwargs):
        self.plot(func, *args, **kwargs)
    return wrapper


class Plots:

    def __init__(self, experiment, fname):
        self.fname = fname
        self.plots = []
        self.figure = None
        # self.trials = list(Experiment.from_db(experiment).trials)
        e = Experiment.from_db(experiment)
        self.trials = list(e.trials)
        print(len(e._trials), len(self.trials))

    @plot
    def golds_purity(self, ax):
        data = []
        for trial in self.trials:
            golds = len(trial.golds)
            purity = trial.score_stats['purity']

            data.append((golds, purity))

        x, y = zip(*data)
        self.pretty(ax, 'Golds', 'Purity', 'Golds v Purity')
        ax.scatter(x, y)

    @plot
    def golds_completeness(self, ax):
        data = []
        for trial in self.trials:
            golds = len(trial.golds)
            completeness = trial.score_stats['completeness']

            data.append((golds, completeness))

        x, y = zip(*data)
        self.pretty(ax, 'Golds', 'Completeness', 'Golds v Completeness')
        ax.scatter(x, y)

    @plot
    def golds_retired(self, ax):
        data = []
        for trial in self.trials:
            x = len(trial.golds)
            y = trial.score_stats['retired']

            data.append((x, y))

        x, y = zip(*data)
        self.pretty(ax, 'Golds', 'Retired', 'Golds v Retired')
        ax.scatter(x, y)

    @plot
    def golds_retired_correct(self, ax):
        data = []
        for trial in self.trials:
            x = len(trial.golds)
            y = trial.score_stats['retired_correct']

            data.append((x, y))

        x, y = zip(*data)
        self.pretty(ax, 'Golds', 'Retired Correct', 'Golds v Retired Correct')
        ax.scatter(x, y)

    @plot
    def mdr_fpr(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['mdr']
            y = trial.score_stats['fpr']

            data.append((x, y))

        x, y = zip(*data)
        self.pretty(ax, 'mdr', 'fpr', 'mdf v fpr')
        ax.scatter(x, y)

    @plot
    def golds_gamma(self, ax):
        data = []
        for trial in self.trials:
            x = len(trial.golds)

            purity = trial.score_stats['purity']
            completeness = trial.score_stats['completeness']
            rc = trial.score_stats['retired']

            y = purity ** 2 + completeness ** 2 + rc ** 2

            data.append((x, y))

        x, y = zip(*data)
        self.pretty(ax, 'Golds', 'Gamma', 'Golds v Gamma')
        ax.scatter(x, y)

    @plot
    def cv_golds_retired(self, ax):
        data = []
        for trial in self.trials:
            x = trial.gold_stats['controversial']['mean']
            y = len(trial.golds)
            c = trial.score_stats['retired']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Average Controversial', 'Golds',
                    'Controversial and Golds vs Retired')

    @plot
    def purity_completeness_golds(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['purity']
            y = trial.score_stats['completeness']
            c = len(trial.golds)

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Purity', 'Completeness',
                    'Purity and Completeness vs Number of Golds')

    @plot
    def purity_completeness_retired(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['purity']
            y = trial.score_stats['completeness']
            c = trial.score_stats['retired']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Purity', 'Completeness',
                    'Purity and Completeness vs Retired')

    @plot
    def cv_cn_purity(self, ax):
        data = []
        for trial in self.trials:
            x = trial.gold_stats['consensus']['mean']
            y = trial.gold_stats['controversial']['mean']
            c = trial.score_stats['purity']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=5, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(
            ax, 'Consensus', 'Controversial',
            'Consensus and Controversial v Purity')

    @plot
    def cv_cn_completeness(self, ax):
        data = []
        for trial in self.trials:
            x = trial.gold_stats['consensus']['mean']
            y = trial.gold_stats['controversial']['mean']
            c = trial.score_stats['completeness']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(
            ax, 'Consensus', 'Controversial',
            'Consensus and Controversial v Completeness')

    @plot
    def cv_cn_retired(self, ax):
        data = []
        for trial in self.trials:
            x = trial.gold_stats['consensus']['mean']
            y = trial.gold_stats['controversial']['mean']
            c = trial.score_stats['retired']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(
            ax, 'Consensus', 'Controversial',
            'Consensus and Controversial v Retired')

    # @plot
    # def plot_2d(self, ax, x_key, y_key, x_name, y_name):
    #     data = []
    #     for trial in self.trials:
    #         x = self.navigate(trial, x_key)
    #         y = self.navigate(trial, y_key)
    #         data.append((x, y))
    #
    #     x, y = zip(*data)
    #
    #     self.pretty(
    #         ax, x_name, y_name,
    #         '%s v %s' % (x_name, y_name))
    #     ax.scatter(x, y)

    #############################################################

    @staticmethod
    def pretty(ax, x, y, title):
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(title)

    @staticmethod
    def navigate(trial, key):
        key = key.split('.')
        value = trial.__dict__
        for k in key:
            value = value[k]

        return value

    def plot(self, func, *args, **kwargs):
        def inner(ax):
            func(self, ax, *args, **kwargs)
        self.plots.append(inner)

    def run(self):
        fig = plt.figure(1)
        self.figure = fig
        j = len(self.plots)
        for i, func in enumerate(self.plots):
            ax = fig.add_subplot(3, 3, i + 1)
            func(ax)

        plt.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.95,
                            hspace=0.4, wspace=0.2)

        if self.fname:
            plt.savefig(self.fname, dpi=300)
        else:
            plt.show()


def main():
    p = Plots(0, None)

    # pylint: disable=E1120
    p.golds_purity()
    p.golds_completeness()
    p.golds_retired()
    p.golds_gamma()
    p.cv_golds_retired()
    p.golds_retired_correct()
    p.purity_completeness_golds()
    p.purity_completeness_retired()
    p.mdr_fpr()
    # p.cv_cn_purity()
    # p.cv_cn_completeness()
    # p.cv_cn_retired()

    p.run()


if __name__ == '__main__':
    main()
