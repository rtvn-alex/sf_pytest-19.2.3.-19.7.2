import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multi_positive(self):
        assert self.calc.multiply(self, 2, 3) == 6

    def test_multi_negative(self):
        assert self.calc.multiply(self, 2, 3) == 5

    def test_div(self):
        assert self.calc.division(self, 15, 5) == 3

    def test_add(self):
        assert self.calc.adding(self, 1, 3) == 4

    def test_sub(self):
        assert self.calc.subtraction(self, 9, 2) == 7
