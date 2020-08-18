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


if __name__ == '__main__':
    unittest.main()
