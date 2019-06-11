import time
import numpy as np
import scipy_python
import _hungarian
import lapsolver
import lap
import lapjv
import hungarian


def algorithm(func, supports_rectangular):

    def decorate(cls):
        cls.name = cls.__name__
        cls.func = func
        cls.supports_rectangular = supports_rectangular
        return cls

    return decorate


class Algorithm:

    def adapt_result(self, result):
        return result

    @classmethod
    def time_algorithm(self, cost_matrix):

        t0 = time.time()
        result = self.func(cost_matrix)
        dt = time.time() - t0
        return result, dt

    def run(self, cost_matrix):

        # get result in scipy form and calculate cost
        result, dt = self.time_algorithm(np.copy(cost_matrix))
        result = self.adapt_result(result)
        obj = cost_matrix[result].sum()

        # verify result
        a, b = result
        if cost_matrix.shape[1] > cost_matrix.shape[0]:
            b, a = result
        assert len(np.unique(a)) == len(a)
        assert (np.sort(b) == np.arange(len(b))).all()

        return dt, obj


@algorithm(scipy_python.linear_sum_assignment, True)
class alg_scipy(Algorithm):
    pass


@algorithm(_hungarian.linear_sum_assignment, True)
class alg_jonkervolgenant(Algorithm):
    pass


@algorithm(lapsolver.solve_dense, True)
class alg_lapsolver(Algorithm):
    pass


@algorithm(hungarian.lap, False)
class alg_hungarian(Algorithm):

    def adapt_result(self, result):
        x = result[0]
        return (np.arange(len(x)), x)


@algorithm(None, True)
class alg_gatagat_lapjv(Algorithm):

    def adapt_result(self, result):
        cost, x, y = result
        return (np.arange(len(x)), x)

    def time_algorithm(self, cost_matrix):

        square = cost_matrix.shape[0] == cost_matrix.shape[1]
        t0 = time.time()
        result = lap.lapjv(cost_matrix, extend_cost=not square)
        dt = time.time() - t0
        return result, dt


@algorithm(lapjv.lapjv, False)
class alg_srcd_lapjv(Algorithm):

    def adapt_result(self, result):
        x, y, _ = result
        return (np.arange(len(x)), x)


algs = [alg_scipy, alg_jonkervolgenant, alg_lapsolver, alg_gatagat_lapjv,
        alg_srcd_lapjv, alg_hungarian]
