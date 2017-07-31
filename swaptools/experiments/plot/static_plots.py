
from swaptools.experiments.db import DB
from swaptools.experiments.experiment import Experiment

import math
import numpy as np
import matplotlib.pyplot as plt


def plot(func):
    def wrapper(self, *args, **kwargs):
        self.plot(func, *args, **kwargs)
    return wrapper


class Plots:
    figures = 0

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
    def ncl_golds_retired_correct(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['ncl_mean']
            c = len(trial.golds)
            y = trial.score_stats['retired_correct']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Number of Classifications', 'Retired Correct',
                    'NCL and Retired Correct vs Golds')

    @plot
    def ncl_golds_retired(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['ncl_mean']
            c = len(trial.golds)
            y = trial.score_stats['retired']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Number of Classifications', 'Retired',
                    'NCL and Retired vs Golds')

    @plot
    def ncl_golds_purity(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['ncl_mean']
            c = len(trial.golds)
            y = trial.score_stats['purity']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Number of Classifications', 'Purity',
                    'NCL and Purity vs Golds')

    @plot
    def ncl_golds_completeness(self, ax):
        data = []
        for trial in self.trials:
            x = trial.score_stats['ncl_mean']
            c = len(trial.golds)
            y = trial.score_stats['completeness']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(ax, 'Number of Classifications', 'Completeness',
                    'NCL and Completeness vs Golds')

    @plot
    def cv_cn_purity(self, ax):
        data = []
        for trial in self.trials:
            x = trial.gold_stats['consensus']['mean']
            y = trial.gold_stats['controversial']['mean']
            c = trial.score_stats['purity']

            data.append((x, y, c))

        x, y, c = zip(*data)

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
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

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
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

        im = ax.scatter(x, y, c=c, s=15, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        self.pretty(
            ax, 'Consensus', 'Controversial',
            'Consensus and Controversial v Retired')

    @plot
    def plot_2d(self, ax, x_key, y_key, axes=None, title=None, s=10):
        if axes is None:
            axes={}

        data = []
        for trial in self.trials:
            x = self.get_value(trial, x_key)
            y = self.get_value(trial, y_key)
            data.append((x, y))

        x, y = zip(*data)
        ax.scatter(x, y, s=s)

        axes = self.axes(x_key, y_key, None, axes)
        if title is None:
            title = '%(x)s vs %(y)s' % axes
        self.pretty(ax, axes['x'], axes['y'], title)

    @plot
    def plot_3d(self, ax, x_key, y_key, c_key, axes=None, title=None, s=15):
        if axes is None:
            axes={}

        data = []
        for trial in self.trials:
            x = self.get_value(trial, x_key)
            y = self.get_value(trial, y_key)
            c = self.get_value(trial, c_key)
            data.append((x, y, c))

        x, y, c = zip(*data)
        im = ax.scatter(x, y, c=c, s=s, cmap='viridis')
        self.figure.colorbar(im, ax=ax)

        axes = self.axes(x_key, y_key, c_key, axes)
        if title is None:
            title = '%(x)s and %(y)s vs %(c)s' % axes
        self.pretty(ax, axes['x'], axes['y'], title)

    #############################################################

    @staticmethod
    def axes(x, y, c, axes):
        if 'x' not in axes:
            axes['x'] = x.split('.')[-1].title()
        if 'y' not in axes:
            axes['y'] = y.split('.')[-1].title()
        if c is not None and 'c' not in axes:
            axes['c'] = c.split('.')[-1].title()

        return axes


    @staticmethod
    def pretty(ax, x, y, title):
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(title)

    @staticmethod
    def get_value(trial, key):
        if key is not None:
            if key == 'golds':
                return len(trial.golds)

            key = key.split('.')
            value = trial.__dict__
            for k in key:
                value = value[k]

            return value

    def plot(self, func, *args, **kwargs):
        def inner(ax):
            func(self, ax, *args, **kwargs)
        self.plots.append(inner)

    def reset(self, fname):
        self.plots = []
        self.fname = fname
        self.figure = None

    def run(self):
        if self.fname is None:
            fig = plt.figure(self.figures)
        else:
            fig = plt.figure(self.figures, figsize=(16, 9))
        self.figures += 1
        self.figure = fig

        x = math.ceil(math.sqrt(len(self.plots)))
        y = math.ceil(len(self.plots) / x)

        for i, func in enumerate(self.plots):
            ax = fig.add_subplot(y, x, i + 1)
            func(ax)

        plt.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.95,
                            hspace=0.4, wspace=0.2)

        if self.fname:
            plt.tight_layout()
            plt.savefig(self.fname, dpi=300)
        else:
            plt.show()


def main():
    p = Plots(0, None)

    # pylint: disable=E1120
    # p.plot_2d('golds', 'score_stats.purity')
    # p.plot_2d('golds', 'score_stats.completeness')
    # p.plot_2d('golds', 'score_stats.retired')
    # p.plot_2d('golds', 'score_stats.retired_correct', {'y': 'Retired Correct'})
    # p.plot_2d('golds', 'score_stats.tpr', {'y': 'TPR'})
    # p.run()
    #
    # p.reset(None)
    # p.plot_3d('gold_stats.controversial.mean', 'golds', 'score_stats.retired',
    #           {'x': 'Controversial'})
    # p.plot_3d('score_stats.purity', 'score_stats.completeness',
    #           'golds')
    # p.plot_3d('score_stats.purity', 'score_stats.completeness',
    #           'score_stats.retired')
    # p.plot_2d('score_stats.mdr', 'score_stats.fpr')
    # p.run()
    #
    # p.reset(None)
    # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
    #           'score_stats.purity',
    #           {'x': 'Controversial', 'y': 'Consensus'})
    # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
    #           'score_stats.completeness',
    #           {'x': 'Controversial', 'y': 'Consensus'})
    # p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
    #           'score_stats.retired',
    #           {'x': 'Controversial', 'y': 'Consensus'})
    # p.run()
    #
    # p.reset(None)

    # p.plot_3d('score_stats.ncl_mean', 'golds', 'score_stats.retired',
    #           {'x': 'NCL'})
    # p.plot_3d('score_stats.ncl_mean', 'golds', 'score_stats.purity',
    #           {'x': 'NCL'})
    # p.plot_3d('score_stats.ncl_mean', 'golds', 'score_stats.completeness',
    #           {'x': 'NCL'})
    # p.run()

    p.reset(None)
    p.plot_2d('score_stats.ncl_mean','score_stats.retired_correct',
              {'x': 'NCL',
               'c': 'Retired Correct'})
    p.plot_2d('golds', 'score_stats.retired_correct', {'c': 'Retired Correct'})
    p.plot_3d('score_stats.ncl_mean', 'golds', 'score_stats.retired_correct',
              {'x': 'NCL',
               'c': 'Retired Correct'})
    p.plot_3d('score_stats.ncl_mean', 'score_stats.retired_correct', 'golds',
              {'x': 'NCL',
               'y': 'Retired Correct'})
    # p.plot_2d('score_stats.ncl_mean', 'golds', 'score_stats.retired',
    #           {'x': 'NCL'})
    # p.plot_2d('score_stats.ncl_mean', 'golds', 'score_stats.purity',
    #           {'x': 'NCL'})
    # p.plot_2d('score_stats.ncl_mean', 'golds', 'score_stats.completeness',
    #           {'x': 'NCL'})
    p.run()


if __name__ == '__main__':
    main()
