#!/usr/bin/env python
"""
Create hdf5 files for testing.
"""
import h5py
import numpy as np

N = 1000

ids = np.arange(N)
data_number = np.random.random_sample(N)
data_vector = np.random.random_sample((N, 2))
data_matrix = np.random.random_sample((N, 2, 2))
toremove = list(np.random.random_integers(low=0, high=N, size=10))


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

    create("full.hdf5", number=True, vector=True, matrix=True)
    create("number.hdf5", number=True)
    create("vector.hdf5", vector=True)
    create("matrix.hdf5", matrix=True)
    create("number_messed.hdf5", number=True, remove=toremove)
    create("vector_messed.hdf5", vector=True, remove=toremove)
    create("matrix_messed.hdf5", matrix=True, remove=toremove)
    create("full_messed_shapes.hdf5", number=False, vector=True, matrix=True,
           mess_shapes=True)
