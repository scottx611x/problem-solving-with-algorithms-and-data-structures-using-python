import unittest
from excercises import Fraction, FractionException


class FractionTests(unittest.TestCase):
    def setUp(self):
        self.fraction = Fraction(1, 2)

    def test___str__(self):
        self.assertEqual(str(self.fraction), "1 / 2")

    def test_get_numerator(self):
        self.assertEqual(self.fraction.get_numerator(), 1)

    def test_get_denominator(self):
        self.assertEqual(self.fraction.get_denominator(), 2)

    def test__gcd_runs_on_init(self):
        self.assertEqual(str(Fraction(6, 12)), "1 / 2")

    def test__eq__(self):
        self.assertEqual(self.fraction, Fraction(1, 2))
        self.assertEqual(self.fraction, Fraction(2, 4))
        self.assertNotEqual(self.fraction, Fraction(3, 4))

    def test__add__(self):
        self.assertEqual(self.fraction + Fraction(4, 8), Fraction(1, 1))

    def test__sub__(self):
        self.assertEqual(self.fraction - Fraction(1, 3), Fraction(1, 6))

    def test_true_disivison(self):
        self.assertEqual(Fraction(2, 4) / self.fraction, Fraction(1, 4))

    def test_fraction_exception_if_non_int(self):
        with self.assertRaises(FractionException):
            Fraction(1.0, 2)

        with self.assertRaises(FractionException):
            Fraction(1, 2.0)

if __name__ == '__main__':
    unittest.main()
