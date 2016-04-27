#!/usr/bin/env python
"""
Print info on datasets in hdf5 (big) file.
"""
import sys
import numpy as np
import imp
import h5py

msg = imp.load_source('msg', '../msg.py')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: ./print file"
        sys.exit(1)

    f = h5py.File(sys.argv[1], 'r')

    print "\nThe following datasets were found in %s:\n" % sys.argv[1]
    msg.list_dataset(f)

    f.close()
