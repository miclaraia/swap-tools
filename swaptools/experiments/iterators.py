
import math
from collections import OrderedDict


class ValueIterator:

    ###############################################################

    def __init__(self, *args):
        values = [(v.name, v) for v in args]
        self.values = OrderedDict(values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __iter__(self):
        for v in self.values.values():
            yield v

    @staticmethod
    def range(start, end, step):
        return _Range(start, end, step)

    @staticmethod
    def list(values):
        return _List(values)

    @staticmethod
    def single(value):
        return _Single(value)

    ###############################################################


class _Iterator:

    def __init__(self, name=None):
        self.name = name
        self.current = None

    def next(self):
        pass

    def step(self):
        self.current = self.next()
        return self.current

    def more(self):
        pass

    def first(self):
        pass

    def reset(self):
        pass

    def count(self):
        pass

    ###############################################################

    def _name(self, name):
        self.name = name

    def __iter__(self):
        return self

    def __next__(self):
        return self.step()


class _Range(_Iterator):

    def __init__(self, start, end, step, name=None):
        super().__init__(name)
        self.start = start
        self.end = end
        self._step = step

        self.current = start

    def next(self):
        return self.current + self._step

    def more(self):
        if type(self.current) is float or type(self.end) is float:
            return self.next() - self.end < 1e-9
        return self.next() <= self.end

    def first(self):
        return self.current == self.start

    def reset(self):
        self.current = self.start

    def count(self):
        return math.floor((self.end - self.start) / self._step) + 1


class _Single(_Iterator):

    def __init__(self, value, name=None):
        super().__init__(name)
        self.current = value

    def more(self):
        return False

    def first(self):
        return True

    def count(self):
        return 1


class _List(_Iterator):

    def __init__(self, values, name=None):
        super().__init__(name)
        self.values = values
        self.i = 0

    @property
    def current(self):
        return self.values[self.i]

    @current.setter
    def current(self, value):
        if value is not None:
            for i, v in enumerate(self.values):
                if v == value:
                    self.i = i
                    return

    def next(self):
        if self.more():
            return self.values[self.i + 1]

    def step(self):
        value = self.next()
        self.i += 1

        return value

    def more(self):
        return self.i + 1 < len(self.values)

    def first(self):
        return self.i == 0

    def reset(self):
        self.i = 0

    def count(self):
        return len(self.values)
