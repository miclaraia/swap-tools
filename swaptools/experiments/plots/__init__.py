
# from swaptools.experiments.experiment import Experiment

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import statistics as st


def plot(func):
    def wrapper(self, *args, **kwargs):
        self.plot(func, *args, **kwargs)
    return wrapper


class Args:

    def __init__(self, defaults=None):
        self.args = {}

        if defaults is None:
            defaults = {}
        self._defaults = defaults

    def __call__(self):
        args = self.defaults()
        args.update(self.args)
        return args

    def __getitem__(self, key):
        return self.args.get(key)

    def __contains__(self, key):
        return key in self.args

    def __setitem__(self, key, value):
        self.args[key] = value

    def get(self, key, *args):
        return self.args.get(key, *args)

    def pop(self, key):
        return self.args.pop(key)

    def update(self, args):
        self.args.update(args)

    def _reset(self):
        self.args = self.defaults()

    def defaults(self):
        return self._defaults.copy()

    def set_defaults(self, defaults):
        self._defaults = {}
        self._defaults.update(defaults)


class Plotter:
    figures = 0

    def __init__(self, experiment, fname):
        self.fname = fname
        self.plots = {0: []}
        self.figure = None

        self.plot_args = Args({'s': 10, 'alpha': 1, 'cmap': 'viridis'})
        self.kwargs = Args()

        self.trials = list(experiment.trials)
        print(len(experiment._trials), len(self.trials))

    @plot
    def plot_2d(
            self, ax, x_key, y_key,
            kwargs):

        kwargs['keys'] = (x_key, y_key)
        pltargs = self.plot_args()

        data = self.get_data()
        x, y = zip(*data)
        ax.scatter(x, y, **pltargs)

        axes = self.axes()
        title = '%(x)s vs %(y)s' % axes
        self.pretty(ax, axes, title)

        return ax

    @plot
    def plot_3d(
            self, ax, x_key, y_key, c_key,
            kwargs):

        kwargs['keys'] = (x_key, y_key, c_key)
        pltargs = self.plot_args()

        data = self.get_data()
        x, y, c = zip(*data)

        print(kwargs())

        cmap = None
        if kwargs.get('discrete') is True:
            cmap = DiscreteColorMap()

            if 'domain' in kwargs:
                domain = kwargs.pop('domain')
            else:
                domain = FD.find_domain(data)
            cmap.domain(domain)

            c = list(c)
            for i, v in enumerate(c):
                c[i] = cmap(v)

            self.color_legend(ax, cmap)

        im = ax.scatter(x, y, c=c, **pltargs)
        if cmap is None:
            self.figure.colorbar(im, ax=ax)

        axes = self.axes()
        title = '%(x)s and %(y)s vs %(c)s' % axes
        self.pretty(ax, axes, title)

        return ax

    @plot
    def plot_kde(
            self, ax, x_key, y_key, c_key,
            kwargs):

        kwargs['keys'] = (x_key, y_key, c_key)

        data = self.get_data()

        if 'domain' in kwargs:
            domain = kwargs['domain']
        else:
            domain = FD.find_domain(data)

        print(domain)
        colors = ['Blues', 'Reds', 'Greens', 'Purples']
        cmap = DiscreteColorMap(colors)
        cmap.domain(domain)

        data = self.get_data()
        x, y, _ = zip(*data)
        x = np.array(x)
        y = np.array(y)
        sns.kdeplot(
            x, y, cmap=cmap(data[0][2]),
            shade=True, shade_lowest=False,
            alpha=.7)

        axes = self.axes()
        title = '%(x)s vs %(y)s kernel density' % axes
        self.pretty(ax, axes, title)
        self.color_legend(ax, cmap)

        return ax

    @plot
    def plot_ebar(
            self, ax, x_key, y_key,
            kwargs):
        """
        Draw an error bar plot. Plots the mean and standard deviation of
        values that share an x-coordinate.
        """

        kwargs['keys'] = (x_key, y_key)
        data = self.get_data()
        pltargs = self.plot_args()

        data = FD.error_bars(data, 0, 1)
        x, y, yerr = zip(*data)

        plt.errorbar(x, y, yerr=yerr, fmt='o')

        axes = self.axes()
        title = '%(x)s vs %(y)s' % axes
        self.pretty(ax, axes, title)

    @plot
    def plot_ebar_d(
            self, ax, x_key, y_key, c_key,
            kwargs):

        kwargs['keys'] = (x_key, y_key, c_key)
        data = self.get_data()
        domain = kwargs.get('domain', FD.find_domain(data))
        pltargs = self.plot_args()

        cmap = DiscreteColorMap()
        cmap.domain(domain)
        self.color_legend(ax, cmap)

        domain_data = FD.bin_data(data, 2)
        print('domain_data: ', domain_data)
        for d, data in domain_data.items():
            data = FD.error_bars(data, 0, 1)
            x, y, yerr = zip(*data)

            plt.errorbar(x, y, c=cmap(d), yerr=yerr, fmt='o')

        axes = self.axes()
        title = '%(x)s vs %(y)s' % axes
        self.pretty(ax, axes, title)


    def bin_reg(self, ax):
        """
        Draw a line following the mean of values that share an x-coordinate
        """
        data = self.get_data()
        bins = FD.bin_data(data)

        line = []
        for x in sorted(bins):
            y = st.mean(bins[x])
            line.append((x, y))

        x, y = zip(*line)
        ax.plot(x, y)


    #############################################################

    def axes(self):
        """
        Define axis labels using the key mapping if it
        is not already specified
        """
        axes = self.kwargs.get('axes', {})
        keys = self.kwargs['keys']

        x, y = keys[:2]
        if 'x' not in axes:
            axes['x'] = x.split('.')[-1].title()
        if 'y' not in axes:
            axes['y'] = y.split('.')[-1].title()
        if len(keys) > 2:
            c = keys[2]
            if c is not None and 'c' not in axes:
                axes['c'] = c.split('.')[-1].title()

        return axes


    @staticmethod
    def pretty(ax, axes, title):
        ax.set_xlabel(axes['x'])
        ax.set_ylabel(axes['y'])
        ax.set_title(title)

    @staticmethod
    def color_legend(ax, cmap):
        patches = []
        for value, color in cmap.cmap.items():
            if color[-1] == 's':
                color = color[:-1].lower()
            patch = mpatches.Patch(color=color, label=value)
            patches.append(patch)
        ax.legend(handles=patches)

    @staticmethod
    def get_value(trial, key):
        """
        Fetch a value from a trial using a key mapping
        """
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

    def get_data(self, kwargs=None):
        """
        Get multiple values from each trial.
        """
        if kwargs is None:
            kwargs = self.kwargs

        keys = kwargs['keys']

        data = []
        for t in self.trials:
            values = []
            for k in keys:
                values.append(self.get_value(t, k))
            data.append(values)

        if 'filter' in self.kwargs:
            print(self.kwargs['filter'])
            data = FD.filter_data(data, self.kwargs['filter'])

        return data

    def plot(self, func, *args, **kwargs):
        plot_args = self.plot_args()
        plot_args.update(kwargs.get('pltargs', {}))
        kwargs['pltargs'] = plot_args

        defaults = self.kwargs.defaults()

        def inner(ax):
            self.kwargs._reset()
            self.kwargs.update(defaults)
            self.kwargs.update(kwargs)
            print(self.kwargs.defaults())
            print(self.kwargs())

            ax = func(self, ax, *args, self.kwargs)

            if 'xlim' in kwargs:
                left, right = kwargs['xlim']
                ax.set_xlim(left, right)
            if 'ylim' in kwargs:
                left, right = kwargs['ylim']
                ax.set_ylim(left, right)
            if 'title' in kwargs:
                ax.set_title(kwargs['title'])

            if kwargs.get('regression') is True:
                self.bin_reg(ax)

        self.plots[self.figures].append(inner)

    def reset(self):
        self.plots = []
        self.figure = None

    def next(self, pltargs=None, kwargs=None):
        self.plot_args._reset()
        if pltargs is not None:
            self.plot_args.update(pltargs)

        if kwargs is None:
            self.kwargs.set_defaults({})
        else:
            self.kwargs.set_defaults(kwargs)

        if len(self.plots[self.figures]) > 0:
            self.figures += 1
            self.plots[self.figures] = []

    def run(self):
        fname = self.fname
        sns.reset_orig()

        for i, plots in self.plots.items():
            if plots == []:
                continue

            print('Plot %d' % i)
            width = math.ceil(math.sqrt(len(plots)))
            height = math.ceil(len(plots) / width)

            if fname is None:
                fig = plt.figure(i)
            else:
                fig = plt.figure(i, figsize=(16, 9))
            plt.clf()

            self.figure = fig
            for j, func in enumerate(plots):
                print(func)
                ax = fig.add_subplot(height, width, j + 1)
                plt.cla()
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
                     axes={'x': 'Bogus Threshold',
                           'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1',
                     'score_stats.retired_correct',
                     axes={'x': 'Bogus Threshold',
                           'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.purity',
                     axes={'x': 'Bogus Threshold',
                           'y': 'Real Threshold'})
        self.plot_3d('thresholds.0', 'thresholds.1', 'score_stats.completeness',
                     axes={'x': 'Bogus Threshold',
                           'y': 'Real Threshold'})
        self.plot_3d(
            'thresholds.0', 'thresholds.1', standard,
            axes={'x': 'Bogus Threshold',
                  'y': 'Real Threshold'})

        self.next()
        self.plot_3d('score_stats.fnr', 'score_stats.fpr', standard)
        self.plot_3d('score_stats.tpr', 'score_stats.tnr', standard)
        self.plot_3d('score_stats.tpr', 'score_stats.fnr', standard)
        self.plot_3d('score_stats.tnr', 'score_stats.fpr', standard)


class DiscreteColorMap:


    def __init__(self, colors=None):
        if colors is None:
            colors = [
                "#9b59b6", "#3498db", "#707070",
                "#e74c3c", "#34495e", "#2ecc71"]
        self.colors = colors
        self.cmap = {}
        self.i = 0

    def __call__(self, value):
        return self.color(value)

    def color(self, value):
        if self.i >= len(self.colors):
            self.i = 0
        if value in self.cmap:
            return self.cmap[value]
        return self._map(value)

    def _map(self, value):
        color = self.colors[self.i]
        self.i += 1

        self.cmap[value] = color
        return color

    def domain(self, values):
        for v in values:
            self._map(v)


class FormatData:

    @staticmethod
    def bin_data(data, index=0):
        # Group the data by their x-coordinates
        bins = {}
        for d in data:
            k = d[index]
            if k not in bins:
                bins[k] = []
            bins[k].append(d)

        return bins

    @classmethod
    def error_bars(cls, data, domain=0, value=1):
        """
        Get the binned data and output each bin's mean and standard deviation

        domain : int
            index of the domain value in the array

        value : int
            index of the range value in the array
        """
        bins = cls.bin_data(data, domain)

        # Sort the data by x-coordinate and calculate the
        # mean and standard deviation in each bin
        out = []
        for d in sorted(bins):
            values = [item[value] for item in bins[d]]
            m = st.mean(values)
            s = st.stdev(values)
            out.append((d, m, s))

        return out

    @staticmethod
    def filter_data(data, condition):
        """
        Filter points from all the data
        """
        return [d for d in data if condition(d)]

    @staticmethod
    def find_domain(data, index=2):
        """
        Determine all the discrete values in the domain along an axis
        """
        domain = []
        for d in data:
            c = d[index]
            if c not in domain and \
                    c + 1 not in domain and \
                    c - 1 not in domain:
                domain.append(c)
        return list(sorted(domain))

    @staticmethod
    def get_value(trial, key):
        """
        Fetch a value from a trial using a key mapping
        """
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

    @classmethod
    def get_data(cls, trials, keys):
        """
        Parse the right data out from the trials. Returns list of tuples,
        where each tuple corresponds to the values in the keys list.
        """

        data = []
        for t in trials:
            values = []
            for k in keys:
                values.append(cls.get_value(t, k))
            data.append(values)

        return data

FD = FormatData
