from enum import Enum, auto

import numpy as np

from ffield import Field
from util import generate_random_binary_polynomial


class Implementation(Enum):
    OLD = auto()
    NEW = auto()


class NTRUParameters:
    def __init__(self, n, p, q, f=None, g=None, r=None, d_f: (int, int) = None, d_g=None, d_r=None,
                 num_iter=1000, choose_minus=True, q_exponent_of=2, implementation=Implementation.OLD):
        # public parameters
        self.N = n
        self.mod_poly = np.poly1d([1] + [0 for _ in range(self.N - 1)] + [-1])
        self.p = p
        self.q = q
        self.field_p = Field(self.p, self.mod_poly)
        self.field_q = Field(self.q, self.mod_poly)

        self.f = f
        self.g = g
        self.r = r
        self.f_p = None
        self.f_q = None
        self.choose_minus = choose_minus
        self.d_r = d_r
        self.implementation = implementation

        self.init_polynomials(num_iter, choose_minus, d_f, d_g, q_exponent_of)

        if self.implementation == Implementation.OLD:
            self.h = self.field_q.poly_mod(self.g * self.f_q)
        elif self.f_q is not None:
            self.h = self.field_q.poly_mod(self.f_q * self.g * p)

    def init_polynomials(self, num_iter, choose_minus, d_f, d_g, q_exponent_of):
        inv_exists = False
        count = 0

        f = None
        while not inv_exists and count < num_iter:
            count += 1

            if self.f is None:
                f = generate_random_binary_polynomial(self.N - 1, choose_minus, d_f)
            else:
                f = self.f

            inv_exists_p = True
            if self.implementation == Implementation.OLD:
                inv_exists_p, self.f_p = self.field_p.poly_inverse(f)

            if self.q % q_exponent_of == 0:
                inv_exists_q, self.f_q = self.field_q.poly_inv_pow_2(f, q_exponent_of)
            else:
                inv_exists_q, self.f_q = self.field_q.poly_inverse(f)

            inv_exists = inv_exists_p and inv_exists_q

        self.f = f

        if not inv_exists:
            raise RuntimeError('Could not generate random f')

        while self.g is None or self.g == np.poly1d(0):
            g = generate_random_binary_polynomial(self.N - 1, choose_minus, d_g)

            if self.implementation == Implementation.NEW:
                exists, _ = self.field_q.poly_inv_pow_2(g, q_exponent_of)
                if exists:
                    self.g = g
            else:
                self.g = g


class NTRU:
    def __init__(self, parameters: NTRUParameters):
        self.parameters = parameters

    def encrypt(self, message: np.poly1d):
        r = self.parameters.r
        while r is None or r == np.poly1d(0):
            r = generate_random_binary_polynomial(self.parameters.N - 1, self.parameters.choose_minus,
                                                  self.parameters.d_r)
        return self.parameters.field_q.poly_mod(self.parameters.p * r * self.parameters.h + message)

    def decrypt(self, cipher_text: np.poly1d):
        a = self.parameters.field_q.poly_mod(self.parameters.f * cipher_text)
        centered_a = self.center_polynomial_q(a)
        prod = self.parameters.field_p.poly_mod(self.parameters.f_p * centered_a)
        return self.center_polynomial_p(prod)

    def center_polynomial_q(self, polynomial: np.poly1d) -> np.poly1d:
        centered = []

        for num in polynomial:
            if num > self.parameters.q // 2:
                num = num - self.parameters.q
            centered.append(num)
        return np.poly1d(centered)

    def center_polynomial_p(self, polynomial: np.poly1d) -> np.poly1d:
        centered = []

        for num in polynomial:
            if num > self.parameters.p // 2:
                num = num - self.parameters.p
            centered.append(num)
        return np.poly1d(centered)
