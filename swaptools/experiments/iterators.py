
import math


class ValueIterator:

    ###############################################################

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
        pass

    def next(self):
        if self.more():
            return self.values[self.i + 1]

    def step(self):
        value = self.next()
        self.i += 1

        return value

    def more(self):
        return self.i + 1 < len(self.values)

    def reset(self):
        self.i = 0

    def count(self):
        return len(self.values)


