import unittest
import numpy as np

from ffield import Field


class NumberInverseTests(unittest.TestCase):
    def test_number_inverse_1(self):
        field = Field(7)
        self.assertEqual(6, field.number_inverse(6))

    def test_number_inverse_2(self):
        field = Field(26)
        self.assertEqual(9, field.number_inverse(3))

    def test_number_inverse_3(self):
        field = Field(177)
        self.assertEqual(103, field.number_inverse(55))


class PolyModTest(unittest.TestCase):
    def test_mod_1(self):
        polynomial = np.zeros(12)
        polynomial[0] = 14
        polynomial[-1] = 47
        polynomial = np.poly1d(polynomial)

        inverse_over = np.zeros(12)
        inverse_over[0] = 1
        inverse_over[-1] = -1

        field = Field(61, np.poly1d(inverse_over))

        self.assertEqual(np.poly1d([0]), field.poly_mod(polynomial))


class PolyDivisionTest(unittest.TestCase):
    def test_division_1(self):
        field = Field(7)
        polynomial = np.poly1d([1, 0, 0])
        divisor = np.poly1d([1, 0])

        expected_quotient = np.poly1d([1, 0])
        expected_remainder = np.poly1d(0)

        self.assertEqual((expected_quotient, expected_remainder), field.divide_poly(polynomial, divisor))

    def test_division_2(self):
        field = Field(7)
        polynomial = np.poly1d([1, 0, 6, 0, 2])
        divisor = np.poly1d([1, 0, 5])

        expected_quotient = np.poly1d([1, 0, 1])
        expected_remainder = np.poly1d([4])

        self.assertEqual((expected_quotient, expected_remainder), field.divide_poly(polynomial, divisor))

    def test_division_3(self):
        field = Field(61)
        polynomial = np.poly1d([-1, -1, 0, -1, 0, 1, 0, 1, 0, 1])
        divisor = np.poly1d([59., 1., 0., 60., 2., 60., 2., 60., 0.])

        expected_quotient = np.poly1d([31., 16.])
        expected_remainder = np.poly1d([45., 30., 15., 0., 15., 0., 16., 1.])

        self.assertEqual((expected_quotient, expected_remainder), field.divide_poly(polynomial, divisor))

    def test_division_4(self):
        field = Field(61)
        polynomial = np.poly1d([39, 47])
        divisor = np.poly1d([48])

        expected_quotient = np.poly1d([58, 48])
        expected_remainder = np.poly1d([0])

        self.assertEqual((expected_quotient, expected_remainder), field.divide_poly(polynomial, divisor))


class PolyInverseTest(unittest.TestCase):
    def test_inverse_1(self):
        polynomial = np.poly1d([1, 0, 1])
        field = Field(3, np.poly1d([1, 0, 2, 1]))

        expected_inverse = np.poly1d([2, 1, 2])

        self.assertEqual((True, expected_inverse), field.poly_inverse(polynomial))

    def test_inverse_example_NTRU_fp(self):
        polynomial = np.poly1d([-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1])
        inverse_over = np.zeros(12)
        inverse_over[0] = 1
        inverse_over[-1] = -1
        field = Field(3, np.poly1d(inverse_over))

        expected_inverse = np.poly1d([1, 0, 1, 0, 1, 2, 2, 2, 1, 0])

        self.assertEqual((True, expected_inverse), field.poly_inverse(polynomial))

    def test_inverse_example_NTRU_fq(self):
        polynomial = np.poly1d([-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1])
        inverse_over = np.zeros(12)
        inverse_over[0] = 1
        inverse_over[-1] = -1
        field = Field(61, np.poly1d(inverse_over))

        expected_inverse = np.poly1d([45, 49, 26, 40, 53, 47, 21, 24, 60, 32, 31])

        self.assertEqual((True, expected_inverse), field.poly_inverse(polynomial))


if __name__ == '__main__':
    unittest.main()
