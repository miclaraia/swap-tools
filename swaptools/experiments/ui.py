
from swap.ui.ui import Interface

import swaptools.experiments.config as config
import swaptools.experiments.db.experiment_data as dbe
import swaptools.experiments.db.plots as plotsdb
from swaptools.experiments.experiment import Experiment


class ExperimentInterface(Interface):
    Experiment = Experiment

    def _from_db(self, name, cutoff):
        return self.Experiment.build_from_db(name, cutoff)

    def _trial_kwargs(self, trial_args):
        pass

    def _build_trial(self, trial_info, golds, scores):
        return self.Experiment.Trial.build_from_db(trial_info, golds, scores)

    def options(self, parser):

        parser.add_argument(
            '--run', action='store_true',
            help=('trials directory, experiment file'))

        parser.add_argument(
            '--cutoff', nargs=1,
            help='p cutoff')

        parser.add_argument(
            '--from-trials', nargs=1,
            metavar='directory with trial files',
            help='load experiment plot data from trial files')

        parser.add_argument(
            '--load', nargs=1,
            metavar='file',
            help='load pickled experiment data')

        parser.add_argument(
            '--save', nargs=1,
            metavar='file',
            help='pickle and save experiment data')

        parser.add_argument(
            '--shell', action='store_true',
            help='Drop to python interpreter after loading experiment')

        parser.add_argument(
            '--plot', nargs=2,
            metavar=('type', 'file'),
            help='Generate experiment plot')

        parser.add_argument(
            '--pow', action='store_true',
            help='controversial and consensus aggregation method')

        parser.add_argument(
            '--multiply', action='store_true',
            help='controversial and consensus aggregation method')

        parser.add_argument(
            '--from-db', action='store_true',
            help='experiment name')

        parser.add_argument(
            '--swap-from-trial', action='store_true')

        parser.add_argument(
            '--trial', nargs='*')

        parser.add_argument(
            '--name', nargs=1, required=True,
            help='Name of experiment')

        parser.add_argument(
            '--save-plot', nargs=1)

        # parser.add_argument(
        #     '--upload', nargs=1,
        #     metavar='directory containing trial files',
        #     help='Upload trials to mongo database')

    def call(self, args):

        name = args.name[0]

        if args.pow:
            config.controversial_version = 'pow'
        elif args.multiply:
            config.controversial_version = 'multiply'

        if args.run:
            e = self._run(name, cutoff, args)

        elif args.from_trials:
            e = self.Experiment.from_trial_export(
                args.from_trials[0],
                cutoff, self.save, self.load)

        elif args.from_db:
            e = self._from_db(name, cutoff)

        elif args.swap_from_trial:
            trial_info = self._trial_kwargs(args.trial)
            trial = self._trial_from_db(trial_info, name)

            swap = self.swap_from_trial(trial)

        elif args.load:
            e = self.load(args.load[0])

        if args.plot:
            self._plot(e, args)

        if args.save_plot:
            self.save_plot(e, args)

        if args.shell:
            import code
            code.interact(local=locals())

        if args.save:
            assert e
            self.save(e, self.f(args.save[0]))

    @classmethod
    def save_plot(cls, e, args):
        name = args.save_plot[0]
        points = e._db_export_plot()
        plotsdb.upload_plot(name, points)

    def _run(self, name, cutoff, args):
        pass

    def _plot(self, e, args):
        assert e
        fname = self.f(args.plot[1])
        type_ = args.plot[0]

        e.plot(type_, fname)

    def _trial_from_db(self, trial_info, name):
        print(trial_info)
        t, g, s = dbe.SingleTrialCursor(name, trial_info).next()
        return self._build_trial(t, g, s)

    def swap_from_trial(self, trial):
        control = Control()
        control.gold_getter.these(trial.golds)
        control.run()

        return control.swap
