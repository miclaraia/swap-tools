
# from swaptools.experiments.experiment import Experiment

import math
import matplotlib.pyplot as plt
import seaborn


def plot(func):
    def wrapper(self, *args, **kwargs):
        self.plot(func, *args, **kwargs)
    return wrapper


class Plotter:
    figures = 0

    def __init__(self, experiment, fname):
        self.fname = fname
        self.plots = {0: []}
        self.figure = None
        # self.trials = list(Experiment.from_db(experiment).trials)
        self.trials = list(experiment.trials)
        print(len(experiment._trials), len(self.trials))

    @plot
    def plot_2d(self, ax, x_key, y_key, axes=None, title=None, s=10):
        if axes is None:
            axes = {}

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
            axes = {}

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
                if type(value) in [list, tuple]:
                    k = int(k)
                value = value[k]

            return value

    def plot(self, func, *args, **kwargs):
        def inner(ax):
            func(self, ax, *args, **kwargs)
        self.plots[self.figures].append(inner)

    def reset(self):
        self.plots = []
        self.figure = None

    def next(self):
        self.figures += 1
        self.plots[self.figures] = []

    def run(self):
        fname = self.fname
        seaborn.reset_orig()

        for i, plots in self.plots.items():
            print('Plot %d' % i)
            width = math.ceil(math.sqrt(len(plots)))
            height = math.ceil(len(plots) / width)

            if fname is None:
                fig = plt.figure(i)
            else:
                fig = plt.figure(i, figsize=(16, 9))

            self.figure = fig
            for j, func in enumerate(plots):
                ax = fig.add_subplot(height, width, j + 1)
                func(ax)

            plt.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.95,
                                hspace=0.4, wspace=0.2)

            if fname is not None:
                plt.savefig(fname % i, dpi=300)


        if fname is None:
            plt.show()

    #########################################################################
    ## Default plots
    # pylint: disable=E1120

    def plot_standard(self, standard):
        self.next()
        self.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.retired',
                     {'x': 'Bogus Threshold',
                      'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1',
                     'score_stats.retired_correct',
                     {'x': 'Bogus Threshold',
                      'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.purity',
                     {'x': 'Bogus Threshold',
                      'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.completeness',
                     {'x': 'Bogus Threshold',
                      'y': 'Real Threshold'})
        self.plot_3d(
            'thresholds.0', 'thresholds.1', standard,
            {'x': 'Bogus Threshold',
            'y': 'Real Threshold'})

        self.next()
        self.plot_3d('score_stats.fnr', 'score_stats.fpr', standard)
        self.plot_3d('score_stats.tpr', 'score_stats.tnr', standard)
        self.plot_3d('score_stats.tpr', 'score_stats.fnr', standard)
        self.plot_3d('score_stats.tnr', 'score_stats.fpr', standard)


# def main():
#     e = Experiment.from_db(1)
#     p = Plotter(e, 'output/plots-gamma-%d')
#
#     # pylint: disable=E1120
#     p.plot_2d('info.gamma', 'score_stats.purity')
#     p.plot_2d('info.gamma', 'score_stats.completeness')
#     p.plot_2d('info.gamma', 'score_stats.retired')
#     p.plot_2d('info.gamma', 'score_stats.retired_correct', {'y': 'Retired Correct'})
#     p.plot_2d('info.gamma', 'score_stats.tpr', {'y': 'TPR'})
#
#     p.next()
#     p.plot_3d('gold_stats.controversial.mean', 'info.gamma', 'score_stats.retired',
#               {'x': 'Controversial'})
#     p.plot_3d('score_stats.purity', 'score_stats.completeness',
#               'info.gamma')
#     p.plot_3d('score_stats.purity', 'score_stats.completeness',
#               'score_stats.retired')
#     p.plot_2d('score_stats.mdr', 'score_stats.fpr')
#
#     p.next()
#     p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
#               'score_stats.purity',
#               {'x': 'Controversial', 'y': 'Consensus'})
#     p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
#               'score_stats.completeness',
#               {'x': 'Controversial', 'y': 'Consensus'})
#     p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
#               'score_stats.retired',
#               {'x': 'Controversial', 'y': 'Consensus'})
#     p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
#               'info.gamma',
#               {'x': 'Controversial', 'y': 'Consensus'})
#     p.plot_3d('gold_stats.controversial.mean', 'gold_stats.consensus.mean',
#               'score_stats.ncl_mean',
#               {'x': 'Controversial', 'y': 'Consensus', 'c': 'NCL'})
#
#     p.next()
#     p.plot_2d('score_stats.ncl_mean','score_stats.retired_correct',
#               {'x': 'NCL',
#                'c': 'Retired Correct'})
#     p.plot_2d('info.gamma', 'score_stats.retired_correct', {'c': 'Retired Correct'})
#     p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.retired_correct',
#               {'x': 'NCL',
#                'c': 'Retired Correct'})
#     p.plot_3d('score_stats.ncl_mean', 'score_stats.retired_correct', 'info.gamma',
#               {'x': 'NCL',
#                'y': 'Retired Correct'})
#
#     p.next()
#     p.plot_2d('score_stats.ncl_mean', 'score_stats.retired',
#               {'x': 'NCL'})
#     p.plot_2d('info.gamma', 'score_stats.retired')
#     p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.retired',
#               {'x': 'NCL'})
#     p.plot_3d('score_stats.ncl_mean', 'score_stats.retired', 'info.gamma',
#               {'x': 'NCL'})
#
#     p.next()
#     p.plot_2d('score_stats.ncl_mean', 'score_stats.purity',
#               {'x': 'NCL'})
#     p.plot_2d('info.gamma', 'score_stats.purity')
#     p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.purity',
#               {'x': 'NCL'})
#     p.plot_3d('score_stats.ncl_mean', 'score_stats.purity', 'info.gamma',
#               {'x': 'NCL'})
#
#     p.next()
#     p.plot_2d('score_stats.ncl_mean', 'score_stats.completeness',
#               {'x': 'NCL'})
#     p.plot_2d('info.gamma', 'score_stats.completeness')
#     p.plot_3d('score_stats.ncl_mean', 'info.gamma', 'score_stats.completeness',
#               {'x': 'NCL'})
#     p.plot_3d('score_stats.ncl_mean', 'score_stats.completeness', 'info.gamma',
#               {'x': 'NCL'})
#     p.run()
#
#
# if __name__ == '__main__':
#     main()
