
from swaptools.experiments.iterators import _Range, _List


class TestRange:

    @staticmethod
    def generate():
        return _Range(2, 8, 2)

    def test_next(self):
        v = self.generate()
        v.current = 4

        assert v.next() == 6
        assert v.current == 4

    def test_step(self):
        v = self.generate()
        v.current = 4

        assert v.step() == 6
        assert v.current == 6

    def test_more_true(self):
        v = self.generate()
        v.current = 4

        assert v.more() is True

    def test_more_true_end(self):
        v = self.generate()
        v.current = 6

        assert v.more() is True

    def test_more_false(self):
        v = self.generate()
        v.current = 8

        assert v.more() is False

    def test_reset(self):
        v = self.generate()
        v.current = 6
        v.reset()

        assert v.current == 2

    def test_count(self):
        v = self.generate()
        assert v.count() == 4


class TestList:

    @staticmethod
    def generate():
        return _List([2, 4, 8])

    def test_next(self):
        v = self.generate()
        v.i = 1

        assert v.next() == 8
        assert v.current == 4

    def test_more_step(self):
        v = self.generate()
        v.i = 1

        assert v.step() == 8
        assert v.current == 8

    def test_more_true(self):
        v = self.generate()
        v.i = 1

        assert v.more() is True

    def test_more_false(self):
        v = self.generate()
        v.i = 2

        assert v.more() is False

    def test_reset(self):
        v = self.generate()

        v.i = 2
        v.reset()

        assert v.i == 0
        assert v.current == 2

    def test_count(self):
        assert self.generate().count() == 3
