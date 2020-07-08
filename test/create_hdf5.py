#!/usr/bin/env python
"""
Create hdf5 files for testing.

Usage:
    ./create_hdf5.py [file no. -- default to 0]
"""
import sys
import h5py
import numpy as np

N = 1000

ids = np.arange(N)
data_number = np.random.random_sample(N)
data_vector = np.random.random_sample((N, 2))
data_matrix = np.random.random_sample((N, 2, 2))
toremove = list(np.random.randint(0, N+1, size=10))


def create(filename, number=False, vector=False, matrix=False, remove=None,
           mess_shapes=False):

    """Create a single hdf5 file.

    Keyword  arguments:
    number -- include data_number in the file (default False)
    vector -- include data_vector in the file (default False)
    matrix -- include data_matrix in the file (default False)
    remove -- remove some "events" (default None)
    """

    remove = remove or []
    n = N - len(remove)

    f = h5py.File(filename, 'w')

    f.create_dataset("ids", (n,), dtype='i')[...] \
        = np.delete(ids, remove)

    if number:
        f.create_dataset("data_number", (n,), dtype='f')[...] \
            = np.delete(data_number, remove)

    if vector:
        f.create_dataset("data_vector", (n, 2), dtype='f')[...] \
            = np.delete(data_vector, remove, 0)

    if matrix:
        f.create_dataset("data_matrix", (n, 2, 2), dtype='f')[...] \
            = np.delete(data_matrix, remove, 0)

    if mess_shapes:
        f.create_dataset("data_number", (n, 2, 2), dtype='f')[...] \
            = np.delete(data_matrix, remove, 0)

    f.close()


if __name__ == '__main__':

    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        sys.exit(1)

    file_label = '0'
    if len(sys.argv) > 1:
        file_label = str(sys.argv[1])

    create("full{}.hdf5".format(file_label),
           number=True, vector=True, matrix=True)
    create("number{}.hdf5".format(file_label),
           number=True)
    create("vector{}.hdf5".format(file_label),
           vector=True)
    create("matrix{}.hdf5".format(file_label),
           matrix=True)
    create("number_messed{}.hdf5".format(file_label),
           number=True, remove=toremove)
    create("vector_messed{}.hdf5".format(file_label),
           vector=True, remove=toremove)
    create("matrix_messed{}.hdf5".format(file_label),
           matrix=True, remove=toremove)
    create("full_messed_shapes{}.hdf5".format(file_label),
           number=False, vector=True, matrix=True, mess_shapes=True)
