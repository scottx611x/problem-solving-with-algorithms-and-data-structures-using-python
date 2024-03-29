import operator


class FractionException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Fraction:
    def __init__(self, numerator, denominator):
        if not all(isinstance(i, int) for i in [numerator, denominator]):
            raise FractionException(
                f"{numerator} / {denominator} is not a valid Fraction"
            )

        if denominator < 0:
            denominator = abs(denominator)
            numerator = numerator * -1

        self.numerator = numerator
        self.denominator = denominator
        self._gcd()

    @property
    def _as_float(self):
        return self.numerator / self.denominator

    def __repr__(self):
        return f"Fraction: {self}"

    def __str__(self):
        return f"{self.numerator} / {self.denominator}"

    def __eq__(self, fraction):
        return (self.numerator == fraction.numerator and
                self.denominator == fraction.denominator)

    def __gt__(self, fraction):
        return self._do_comparison(fraction, operator.gt)

    def __ge__(self, fraction):
        return self._do_comparison(fraction, operator.ge)

    def __lt__(self, fraction):
        return self._do_comparison(fraction, operator.lt)

    def __le__(self, fraction):
        return self._do_comparison(fraction, operator.le)

    def __add__(self, fraction):
        return self._do_operation(fraction, operator.add)

    def __iadd__(self, fraction):
        new_numerator, new_denominator = self._do_operation(
            fraction, operator.add, values_only=True
        )
        self.numerator = new_numerator
        self.denominator = new_denominator
        self._gcd()
        return self

    def __radd__(self, fraction):
        return fraction + self

    def __sub__(self, fraction):
        return self._do_operation(fraction, operator.sub)

    def __div__(self, fraction):
        return self._do_operation(fraction, operator.floordiv)

    def __truediv__(self, fraction):
        return self.__div__(fraction)

    def _do_operation(self, fraction, op, values_only=False):
        new_numerator = op(self.numerator * fraction.denominator,
                           self.denominator * fraction.numerator)
        new_denominator = self.denominator * fraction.denominator
        if values_only:
            return new_numerator, new_denominator
        return Fraction(new_numerator, new_denominator)

    def _do_comparison(self, fraction, op):
        return op(self._as_float, fraction._as_float)

    def _gcd(self):
        n = self.numerator
        m = self.denominator
        while n % m != 0:
            old_m = m
            m = n % old_m
        self.numerator = self.numerator // m
        self.denominator = self.denominator // m

    def get_numerator(self):
        return self.numerator

    def get_denominator(self):
        return self.denominator

