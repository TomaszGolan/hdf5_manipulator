"""
HDF5 files tools for HDF5 Manipulator
"""

import h5py


def load(filename):

    """Load hdf5 file to data dictionary and return it.

    Keyword arguments:
    filename -- the full path to hdf5 file
    """

    f = h5py.File(filename, 'r')

    data = {}

    for key in f:
        data[key] = f[key][...]

    f.close()

    return data


def save(filename, data):

    """Create hdf5 file with given data.

    Keyword arguments:
    filename -- the full path to hdf5 file
    data -- dictionary with data
    """

    f = h5py.File(filename, 'w')

    for key in data:
        f.create_dataset(key, data[key].shape, dtype=data[key].dtype)[...] \
            = data[key]

    f.close()


def save_subset(filename, data, begin, end):

    """Create hdf5 file with subset [begin, end) of given data.

    Keyword arguments:
    filename -- the full path to hdf5 file
    data -- dictionary with data
    begin -- start saving from index=i
    end -- finish savin at index=end
    """

    subset = {}

    for key in data:
        subset[key] = data[key][begin:end]

    save(filename, subset)
