#!/usr/bin/env python
"""
Check if two hdf5 files are the same.
"""
import sys
import h5py
import numpy as np
import argparse
import imp

hdf5 = imp.load_source('hdf5', '../hdf5.py')
msg = imp.load_source('msg', '../msg.py')
check = imp.load_source('check', '../check.py')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: ./diff file1 file2"
        sys.exit(1)

    data1 = hdf5.load(sys.argv[1])
    data2 = hdf5.load(sys.argv[2])

    print "\nThe following datasets were found in %s:\n" % sys.argv[1]
    msg.list_dataset(data1)
    print "\nThe following datasets were found in %s:\n" % sys.argv[2]
    msg.list_dataset(data2)

    check.check_keys(data1, data2)

    if check.get_size(data1) != check.get_size(data2):
        msg.error("Different number of entries.")
        sys.exit(1)

    check.check_shapes(data1, data2)

    for key in data1:
        if not np.equal(data1[key], data2[key]).all():
            msg.error("Different entries for dataset: %s" % key)
            sys.exit(1)

    msg.info("Files are the same.")
