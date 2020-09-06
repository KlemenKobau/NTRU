from collections import defaultdict

import itertools
import numpy as np

from ntru import NTRU, NTRUParameters


def auxiliary_function(poly: np.poly1d, res_len: int) -> tuple:
    out = np.zeros(res_len, dtype=np.int)

    for i, num in enumerate(poly):
        out[i + res_len - poly.order - 1] = num > 0

    return tuple(out)


def iter_polynomial(rank: int):
    for comb in itertools.product([-1, 0, 1], repeat=rank + 1):
        poly = np.poly1d(comb)
        if poly != np.poly1d(0):
            yield np.poly1d(poly)


def meet_in_the_middle(n, public_key, ntru: NTRU):
    table = defaultdict(list)

    def test_key(poly_a, polynomial):
        if polynomial in table[poly_a]:
            return False, None
        table[poly_a].append(polynomial)

        if len(table[poly_a]) > 1:
            for first, second in itertools.combinations(table[poly_a], 2):
                combined = ntru.parameters.field_q.poly_mod(first + second)
                combined = ntru.center_polynomial_q(combined)
                test = ntru.parameters.field_q.poly_mod(combined * public_key)
                test = ntru.center_polynomial_q(test)

                # print('q:', ntru.parameters.q)
                # print(first)
                # print(second)
                # print('computed:')
                #
                # print(repr(combined))
                # print('------------------')
                if combined == np.poly1d(0):
                    continue
                for i in test:
                    if i not in [0, 1]:
                        break
                else:
                    if combined == ntru.parameters.f:
                        print('Found candidate:')
                        print(combined)
                        print('First')
                        print(first)
                        print('Second')
                        print(second)
                        print('Hash')
                        print(poly_a)
                        return True, combined

        return False, None

    polynomials = iter_polynomial((n - 1) // 2)
    bigger_by = np.poly1d([1] + [0 for _ in range((n - 1) // 2)])

    for poly in polynomials:
        small_poly = ntru.center_polynomial_q(poly)
        big_poly = ntru.parameters.field_q.poly_mod(small_poly * np.poly1d(bigger_by))

        small_aux = ntru.parameters.field_q.poly_mod(small_poly * ntru.parameters.h)
        small_aux = ntru.center_polynomial_q(small_aux)
        small_aux = auxiliary_function(small_aux, n)
        res, key = test_key(small_aux, small_poly)
        if res:
            print('Found key:')
            print(key)
            break

        big_aux = ntru.parameters.field_q.poly_mod(- big_poly * ntru.parameters.h)
        big_aux = ntru.center_polynomial_q(big_aux)
        big_aux = auxiliary_function(big_aux, n)
        res, key = test_key(big_aux, big_poly)
        if res:
            print('Found key:')
            print(key)
            break

    print('Truth:')
    print(ntru.parameters.f)

if __name__ == '__main__':
    parameters = NTRUParameters(7, 3, 61, choose_minus=False)
    ntru = NTRU(parameters)

    assert ntru.decrypt(ntru.encrypt(np.poly1d([1, 1, 1, 1]))) == np.poly1d([1, 1, 1, 1])
    meet_in_the_middle(ntru.parameters.N, ntru.parameters.h, ntru)
