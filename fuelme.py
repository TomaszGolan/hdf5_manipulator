#!/usr/bin/env python
"""
Add metadata required by Fuel to hdf5 file.
"""
import sys
import h5py
from fuel.datasets.hdf5 import H5PYDataset
import check
import msg


def usage():
    print "usage: ./fuelme.py file train_frac val_frac"
    sys.exit(1)


def get_fractions():
    try:
        return float(sys.argv[2]), float(sys.argv[3])
    except:
        usage()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()

    train_frac, val_frac = get_fractions()

    if train_frac + val_frac > 1.0:
        msg.error("Total fraction must be <= 1.0")
        sys.exit(1)

    f = h5py.File(sys.argv[1], 'r+')

    print "\nThe following datasets were found in %s:\n" % sys.argv[1]
    msg.list_dataset(f)

    N = check.get_size(f)
    nof_train = int(train_frac * N)
    nof_val = int(val_frac * N)
    nof_test = N - nof_train - nof_val

    print "\nThe following split will be used:\n"
    print "\t - training: %d entries" % nof_train
    print "\t - validation: %d entries" % nof_val
    print "\t - testing: %d entries" % nof_test

    train_dict = {name: (0, nof_train)
                  for name in f.keys()}
    valid_dict = {name: (nof_train, nof_train + nof_val)
                  for name in f.keys()}
    test_dict = {name: (nof_train + nof_val, N)
                 for name in f.keys()}

    split_dict = {
        'train': train_dict,
        'valid': valid_dict,
        'test': test_dict
    }

    f.attrs['split'] = H5PYDataset.create_split_array(split_dict)

    f.close()
