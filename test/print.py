#!/usr/bin/env python
"""
Print info on datasets in hdf5 file.
"""
import sys
import numpy as np
import imp

hdf5 = imp.load_source('hdf5', '../hdf5.py')
msg = imp.load_source('msg', '../msg.py')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: ./print file"
        sys.exit(1)

    print "\nThe following datasets were found in %s:\n" % sys.argv[1]
    msg.list_dataset(hdf5.load(sys.argv[1]))
