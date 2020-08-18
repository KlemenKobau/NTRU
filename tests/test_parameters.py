import unittest
import numpy as np

from ntru import NTRU, NTRUParameters


class NTRUEncryptTest(unittest.TestCase):
    def test_f_generation(self):

        for i in range(1000):
            parameters = NTRUParameters(107, 7, 67, d_f=(15, 14), d_g=(12, 12), d_r=(5, 5))
            if i % 100 == 0:
                print('Iteration:', i)

            ntru = NTRU(parameters)
            f = ntru.parameters.f
            f_p = ntru.parameters.f_p
            f_q = ntru.parameters.f_q
            product_p = ntru.parameters.field_p.poly_mod(f * f_p)
            product_q = ntru.parameters.field_q.poly_mod(f * f_q)

            self.assertEqual(np.poly1d(1), product_p)
            self.assertEqual(np.poly1d(1), product_q)

    def test_algorithm_no_salt(self):
        text = np.poly1d(np.ones(40))
        salt = np.poly1d(1)
        for i in range(1000):
            parameters = NTRUParameters(107, 7, 67, d_f=(15, 14), d_g=(12, 12), r=salt)
            if i % 100 == 0:
                print('Iteration:', i)

            ntru = NTRU(parameters)
            cipher = ntru.encrypt(text)
            decrypt = ntru.decrypt(cipher)

            self.assertEqual(text, decrypt)

    def test_algorithm(self):
        text = np.poly1d(np.ones(40))
        num_iter = 1000
        count = 0
        for i in range(num_iter):
            parameters = NTRUParameters(107, 7, 67, d_f=(15, 14), d_g=(12, 12), d_r=(5, 5))
            if i % 100 == 0:
                print('Iteration:', i)

            ntru = NTRU(parameters)
            cipher = ntru.encrypt(text)
            decrypt = ntru.decrypt(cipher)

            if text == decrypt:
                count += 1

        print(count / num_iter)
        self.assertTrue(count / num_iter > 0.6)


if __name__ == '__main__':
    unittest.main()
