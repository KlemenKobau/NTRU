import numpy as np
import logging

LOG = logging.getLogger(__name__)


class Field:
    def __init__(self, mod_number=2, main_poly: np.poly1d = None):
        self.mod_number = mod_number

        if main_poly is not None:
            self.main_poly = self._poly_number_mod(main_poly)

    def number_mod(self, number):
        return (number + self.mod_number) % self.mod_number

    def number_inverse(self, number):
        if self.mod_number <= number:
            LOG.error('Number not present in the field.')
            raise RuntimeError('Number not present in the field.')

        if number < 0:
            number = self.number_mod(number)

        s_0 = 0
        s_1 = 1
        r_0 = self.mod_number
        r_1 = number

        while r_1 != 1:
            if r_1 == 0:
                LOG.error('Cannot invert')
                raise RuntimeError('Cannot invert')

            k = r_0 // r_1

            s_0, s_1 = s_1, self.number_mod(s_0 - k * s_1)
            r_0, r_1 = r_1, r_0 % r_1

        return s_1

    def _poly_number_mod(self, poly):
        return np.poly1d(list(map(lambda x: self.number_mod(x), poly)))

    def poly_mod(self, poly):
        _, remainder = self.divide_poly(poly, self.main_poly)
        return remainder

    def divide_poly(self, poly: np.poly1d, poly_div: np.poly1d):
        if poly_div == np.poly1d(0):
            raise RuntimeError('Dividing by zero polynomial')

        remainder = self._poly_number_mod(poly)
        poly_div = self._poly_number_mod(poly_div)

        # starts with x^n
        quotient = [0 for _ in range(poly.order + 1)]

        while poly_div.order <= remainder.order and remainder != np.poly1d(0):
            multi = self.number_mod(self.number_inverse(poly_div[poly_div.order]) * remainder[remainder.order])
            order_diff = remainder.order - poly_div.order
            order_diff_poly = np.poly1d([1 if i == 0 else 0 for i in range(order_diff + 1)])
            divisor = self._poly_number_mod(poly_div * multi * order_diff_poly)

            quotient[len(quotient) - 1 - order_diff] = self.number_mod(multi)

            remainder = self._poly_number_mod(remainder - divisor)

        return self._poly_number_mod(quotient), self._poly_number_mod(remainder)

    def poly_inverse(self, poly: np.poly1d, verbose=False) -> (bool, np.poly1d):
        s_0 = np.poly1d(0)
        s_1 = np.poly1d(1)

        r_0 = self._poly_number_mod(self.main_poly)
        r_1 = self._poly_number_mod(poly)

        if verbose:
            print("mod number:", self.mod_number)
            print("remainder:")
            print(r_0)
            print("s:")
            print(s_0)
            print("---------------------------------")

            print("mod number:", self.mod_number)
            print("remainder:")
            print(r_1)
            print("s:")
            print(s_1)
            print("---------------------------------")

        while r_1 != np.poly1d([0]):
            koef_poly, remainder = self.divide_poly(r_0, r_1)

            s_0, s_1 = s_1, self._poly_number_mod(np.polysub(s_0, self._poly_number_mod(np.polymul(koef_poly, s_1))))
            r_0, r_1 = r_1, remainder

            if verbose:
                print("remainder:")
                print(r_1)
                print("s:")
                print(s_1)
                print("koef:")
                print(koef_poly)
                print("---------------------------------")

        if r_0.order != 0:
            return False, None

        return True, self.poly_mod(s_0 * self.number_inverse(r_0[0]))