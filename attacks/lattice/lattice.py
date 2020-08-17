import numpy as np
import olll

from ntru import NTRUParameters, NTRU


def lattice_attack(public_key: np.poly1d, q: int, n: int, lam):
    H = np.zeros((n, n))
    poly_list = list(public_key)

    for i in reversed(range(n)):
        H[:, i] = np.array(poly_list).T
        poly_list = poly_list[1:] + [poly_list[0]]

    Q = np.eye(n) * q
    I = np.eye(n) * lam
    O = np.zeros_like(H)

    whole = np.block([[I, H], [O, Q]])
    return np.array(olll.reduction(whole, 0.9))


def check_for_public_key(private_key: np.poly1d, reduced_basis: np.ndarray):
    for column in reduced_basis[:reduced_basis.shape[1]//2, :].T:
        for i in range(reduced_basis.shape[1]//2):
            increase_by = np.zeros(reduced_basis.shape[1]//2)
            increase_by[-(i + 1)] = 1
            increase_by = np.poly1d(increase_by)
            polynomial = np.poly1d(column) * increase_by

            if polynomial.order > reduced_basis.shape[1]//2 - 1:
                continue

            print('Testing:')
            print(polynomial)
            print('Truth:')
            print(private_key)
            print('-----------------------------------------------')

            if private_key == polynomial:
                print('Found key')
                return

    print('Key not found')


if __name__ == '__main__':
    PARAMETERS = NTRUParameters(17, 17, 61, d_f=(3,0), d_g=(2,0), d_r=(3,0))
    ntru = NTRU(PARAMETERS)

    text = ntru.parameters.field_p.poly_mod(np.poly1d([1, 1, 5, 1]))
    text = ntru.center_polynomial_p(text)
    assert ntru.decrypt(ntru.encrypt(text)) == text
    lam = np.linalg.norm(ntru.parameters.g) / np.linalg.norm(ntru.parameters.f)
    new_basis = lattice_attack(ntru.parameters.h, ntru.parameters.q, ntru.parameters.N, lam)
    check_for_public_key(ntru.parameters.f, new_basis)