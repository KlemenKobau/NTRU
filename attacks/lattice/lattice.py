import numpy as np
import olll

from ntru import NTRUParameters, NTRU


def lattice_attack(public_key: np.poly1d, q: int, n: int, first):
    H = np.zeros((n, n))
    poly_list = np.zeros(n)
    for i, num in enumerate(public_key):
        poly_list[i] = num

    for i in reversed(range(n)):
        H[:, i] = np.array(poly_list).T
        poly_list = np.roll(poly_list,-1)

    Q = np.eye(n) * q
    I = np.eye(n)
    O = np.zeros_like(H)

    whole = np.block([[I, H], [O, Q]])

    if first:
        print('Public key')
        print(public_key)
        print(whole)
    return np.array(olll.reduction(whole, 0.9))


def check_for_public_key(private_key: np.poly1d, reduced_basis: np.ndarray):
    for column in reduced_basis[:reduced_basis.shape[1] // 2, :].T:
        for i in range(reduced_basis.shape[1] // 2):
            increase_by = np.zeros(reduced_basis.shape[1] // 2)
            increase_by[-(i + 1)] = 1
            increase_by = np.poly1d(increase_by)
            polynomial = np.poly1d(column) * increase_by

            if polynomial.order > reduced_basis.shape[1] // 2 - 1:
                continue

            # print('Testing:')
            # print(polynomial)
            # print('Truth:')
            # print(private_key)
            # print('-----------------------------------------------')

            if private_key == polynomial:
                print('Found key')
                return True
    return False


if __name__ == '__main__':
    PARAMETERS = NTRUParameters(7, 3, 61, d_f=(2, 0), d_g=(2, 0), d_r=(3, 0))
    ntru = NTRU(PARAMETERS)

    text = ntru.parameters.field_p.poly_mod(np.poly1d([1, 1, 1, 1]))
    text = ntru.center_polynomial_p(text)
    assert ntru.decrypt(ntru.encrypt(text)) == text
    new_basis = lattice_attack(ntru.parameters.h, ntru.parameters.q, ntru.parameters.N, True)

    count = 0
    while not check_for_public_key(ntru.parameters.f, new_basis) and count < 100:
        new_basis = lattice_attack(ntru.parameters.h, ntru.parameters.q, ntru.parameters.N, False)
        count += 1
        if count % 10 == 0:
            print('Count:', count)
    print(new_basis)
    print()
