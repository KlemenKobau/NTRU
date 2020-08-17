import numpy as np


def generate_random_polynomial(rank: int, low, high) -> np.poly1d:
    rng = np.random.default_rng()
    rand_array = rng.integers(low, high, size=rank + 1)
    return np.poly1d(rand_array)


def generate_random_binary_polynomial(rank: int, choose_minus=True, num_ones_neg_ones: (int, int) = None) -> np.poly1d:
    """
    DOES NOT HAVE LEADING 1
    """
    choices = [-1, 0, 1]
    if not choose_minus:
        choices = [0, 1]

    rng = np.random.default_rng()

    if num_ones_neg_ones is None:
        rand_polynomial = rng.choice(choices, rank + 1)
    else:
        rand_polynomial = np.zeros(rank + 1)
        num_ones, num_neg_ones = num_ones_neg_ones
        if num_ones + num_neg_ones > rank + 1:
            raise RuntimeError('Not enough space')
        places = np.arange(rank + 1)
        places_for_ones = rng.choice(places, num_ones, replace=False)
        rand_polynomial[places_for_ones] = 1

        places_for_neg_ones = rng.choice(places[np.logical_not(rand_polynomial)], num_neg_ones, replace=False)
        rand_polynomial[places_for_neg_ones] = -1

    return np.poly1d(rand_polynomial)

if __name__ == '__main__':
    print(generate_random_binary_polynomial(10, num_ones_neg_ones=(3,4)))