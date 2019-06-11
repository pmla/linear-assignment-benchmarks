import numpy as np
from algorithms import algs
from costmatrices import generators


def get_results(num_it, shape, algs, generator):

    times = []
    results = []
    for alg in algs:
        if shape[0] != shape[1] and not alg.supports_rectangular:
            times.append([float("inf")] * num_it)
            results.append([float("inf")] * num_it)
        else:
            data = [alg().run(c) for c in generator(num_it, shape)]
            dt, obj = zip(*data)
            times.append(dt)
            results.append(obj)

    times = np.mean(times, axis=1)
    errors = results - np.min(results, axis=0)
    error_sums = np.sum(errors, axis=1)
    return times, error_sums


def pretty_format(t, e):

    missing = "---------"
    if t == float("inf"):
        return missing, missing
    elif e == 0:
        return "%.3e" % t, "zero".rjust(9)
    else:
        return "%.3e" % t, "%.3e" % e


def run():
    num_it = 10
    shapes = [(20, 20), (20, 40)]
    for shape in shapes:

        heading = "mean time (s)    error sum    status"
        if shape[0] == shape[1]:
            print(("square tests: " + str(shape)).ljust(30) + heading)
        else:
            print(("retangular tests: " + str(shape)).ljust(30) + heading)
        print("=" * 66 + "\n")

        for generator in generators:
            print(' ' * 4, generator.__name__)

            times, errors = get_results(num_it, shape, algs, generator)

            for alg, mtime, err in zip(algs, times, errors):

                passed = mtime < float("inf") and err == 0

                name = alg.__name__[4:]
                tstr, estr = pretty_format(mtime, err)
                status = ['fail', 'pass'][passed]

                spaces = [8, 2, 8, 6, 0]
                values = [name.ljust(20), tstr, estr, status]
                line = ''.join([' ' * a + b for a, b in zip(spaces, values)])
                print(line)
            print()


if __name__ == "__main__":
    run()
