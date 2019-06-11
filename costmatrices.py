import numpy as np
from scipy.spatial.distance import cdist


def random_uniform(n, shape):
    np.random.seed(0)
    for i in range(n):
        yield np.random.uniform(-20, 20, shape)


def random_logarithmic(n, shape):
    np.random.seed(0)
    for i in range(n):
        yield 10**np.random.uniform(-20, 20, shape)


def random_integer(n, shape):
    np.random.seed(0)
    for i in range(n):
        yield np.random.randint(-20, 20, shape)


def random_spatial(n, shape):
    np.random.seed(0)
    for i in range(n):
        P = np.random.uniform(-1, 1, size=(shape[0], 2))
        Q = np.random.uniform(-1, 1, size=(shape[1], 2))
        cost_matrix = cdist(P, Q, 'sqeuclidean')
        assert cost_matrix.shape == shape
        yield cost_matrix

generators = [random_uniform, random_spatial, random_logarithmic,
              random_integer]
