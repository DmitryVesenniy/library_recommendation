import unittest

import numpy as np
from scipy import sparse


# class TestStringMethods(unittest.TestCase):
#
#     def test_create_books(self):
#         a = sparse.csr_matrix([[0, 0, 2], [1, 3, 8]])
#         sums = a.sum(axis=0).A1
#         counts = np.diff(a.indptr)
#
#         averages = (a.sum(0) / a.shape[0]).tolist()
#
#         mean = list(averages[0])
#         self.assertTrue(mean == [0.5, 1.5, 5])


def test_create_books():
    a = sparse.csr_matrix([[0, 0, 2], [1, 3, 8]])
    sums = a.sum(axis=0).A1
    counts = np.diff(a.indptr)
    averages = (a.sum(0) / a.shape[0]).A
    print("averages: ", averages)

    mean = averages

    print(mean)

    print(mean == [0.5, 1.5, 5])


if __name__ == '__main__':
    # unittest.main()
    test_create_books()
