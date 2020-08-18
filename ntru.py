import numpy as np

from ffield import Field
from util import generate_random_binary_polynomial


class NTRUParameters:
    def __init__(self, n, p, q, f=None, g=None, r=None, d_f: (int, int) = None, d_g=None, d_r=None,
                 num_iter=1000, choose_minus=True):
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

        self.init_polynomials(num_iter, choose_minus, d_f, d_g, d_r)
        self.h = self.field_q.poly_mod(self.g * self.f_q)

    def init_polynomials(self, num_iter, choose_minus, d_f, d_g, d_r):
        inv_exists = False
        count = 0

        while not inv_exists and count < num_iter:
            count += 1
            if self.f is None:
                self.f = generate_random_binary_polynomial(self.N - 1, choose_minus, d_f)

            inv_exists_p, self.f_p = self.field_p.poly_inverse(self.f)

            if self.q % self.p == 0:
                inv_exists_q, self.f_q = self.field_q.poly_inv_pow_2(self.f, self.p)
            else:
                inv_exists_q, self.f_q = self.field_q.poly_inverse(self.f)

            inv_exists = inv_exists_p and inv_exists_q

            if not inv_exists:
                self.f = None

        if not inv_exists:
            raise RuntimeError('Could not generate random f')

        while self.g is None or self.g == np.poly1d(0):
            self.g = generate_random_binary_polynomial(self.N - 1, choose_minus, d_g)


class NTRU:
    def __init__(self, parameters: NTRUParameters):
        self.parameters = parameters

    def encrypt(self, message: np.poly1d):
        r = self.parameters.r
        while r is None or r == np.poly1d(0):
            r = generate_random_binary_polynomial(self.parameters.N - 1, self.parameters.choose_minus, self.parameters.d_r)
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
