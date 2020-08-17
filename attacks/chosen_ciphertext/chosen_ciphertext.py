import numpy as np
import itertools

from ntru import NTRU, NTRUParameters


def get_k(rank: int, max_non_zero: int):
    for num_places in range(1, max_non_zero + 1):
        for place_selection in itertools.combinations(range(rank+1), num_places):
            for combinations in itertools.product([1, -1], repeat=num_places):
                out = np.zeros(rank + 1)

                for i, one_or_min_one in enumerate(combinations):
                    out[place_selection[i]] = one_or_min_one

                yield np.poly1d(out)


def get_c(p, q):
    c = q // 4 + 1
    c = c + (p - c % p)
    while c < q // 2:
        yield np.poly1d(c)
        c = c + p


def get_decrypted_chosen(ntru: NTRU):
    h = ntru.parameters.h
    q = ntru.parameters.q
    p = ntru.parameters.p

    for k in get_k(ntru.parameters.N - 1, 5):
        for c in get_c(p, q):
            chosen_ciphertext = h * c + c - q * k
            decrypted = ntru.decrypt(chosen_ciphertext)
            num_inv = ntru.parameters.field_p.number_inverse(-q)
            decrypted = decrypted * num_inv
            exists, inv = ntru.parameters.field_p.poly_inverse(decrypted)
            if not exists:
                continue
            f_candidate = ntru.parameters.field_p.poly_mod(k * inv)
            f_candidate = ntru.center_polynomial_p(f_candidate)
            # print('Truth:')
            # print(ntru.parameters.f)
            # print('Candidate:')
            # print(f_candidate)
            # print('---------------------------------------------------')

            if f_candidate == ntru.parameters.f:
                print('Key found')
                return


if __name__ == '__main__':
    PARAMETERS = NTRUParameters(15, 3, 61)
    ntru = NTRU(PARAMETERS)
    get_decrypted_chosen(ntru)
