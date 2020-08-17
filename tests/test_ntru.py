import unittest
import numpy as np

from ntru import NTRU, NTRUParameters

PARAMETERS = NTRUParameters(11, 3, 61, np.poly1d([-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1]),
                            np.poly1d([-1, -1, 0, -1, 0, 1, 0, 1, 0, 1]),
                            np.poly1d([-1, 0, 1, 0, 0, 1, -1, 0, 0, 1]))


class NTRUEncryptTest(unittest.TestCase):
    def test_getting_h(self):
        ntru = NTRU(PARAMETERS)
        expected_h = np.poly1d([11, 49, 25, 46, 28, 53, 31, 36, 32, 5, 50])

        self.assertEqual(expected_h, ntru.parameters.h)

    def test_getting_cipher_text(self):
        ntru = NTRU(PARAMETERS)
        message = np.poly1d([1, 0, 0, -1, 1, 0, 1, 1])
        expected_cipher_text = np.poly1d([11, 46, 52, 35, 30, 26, 35, 32, 18, 56, 28])

        self.assertEqual(expected_cipher_text, ntru.encrypt(message))

    def test_decrypting(self):
        ntru = NTRU(PARAMETERS)
        cipher_text = np.poly1d([11, 46, 52, 35, 30, 26, 35, 32, 18, 56, 28])
        expected_message = np.poly1d([1, 0, 0, -1, 1, 0, 1, 1])

        self.assertEqual(expected_message, ntru.decrypt(cipher_text))

    def test_ntru_1(self):
        parameters = NTRUParameters(10, 17, 139, choose_minus=False)
        ntru = NTRU(parameters)
        text = np.poly1d([2, 5, 6, 3, 7, 5, 3, 7, 2, 4, 7, 8, 9])
        text = ntru.parameters.field_p.poly_mod(text)
        text = ntru.center_polynomial_p(text)

        cipher = ntru.encrypt(text)
        decrypted = ntru.decrypt(cipher)

        if text != decrypted:
            print('Text:')
            print(text)
            print('Decrypted:')
            print(decrypted)

        self.assertEqual(text, decrypted)

    def test_ntru_2(self):
        parameters = NTRUParameters(107, 3, 67, choose_minus=False)
        ntru = NTRU(parameters)
        text = np.poly1d(np.poly1d(np.ones(1)))
        text = ntru.parameters.field_p.poly_mod(text)
        text = ntru.center_polynomial_p(text)

        cipher = ntru.encrypt(text)
        decrypted = ntru.decrypt(cipher)

        if text != decrypted:
            print('Text:')
            print(text)
            print('Decrypted:')
            print(decrypted)

        self.assertEqual(text, decrypted)


if __name__ == '__main__':
    unittest.main()
