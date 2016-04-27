#!/usr/bin/env python
"""
Check if two hdf5 (big) files are the same.
"""
import sys
import h5py
import numpy as np
import argparse
import imp

msg = imp.load_source('msg', '../msg.py')
check = imp.load_source('check', '../check.py')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: ./diff file1 file2"
        sys.exit(1)

    in1 = h5py.File(sys.argv[1], 'r')
    in2 = h5py.File(sys.argv[2], 'r')

    print "\nThe following datasets were found in %s:\n" % sys.argv[1]
    msg.list_dataset(in1)
    print "\nThe following datasets were found in %s:\n" % sys.argv[2]
    msg.list_dataset(in2)

    check.check_keys(in1, in2)

    check.same_sizes(in1, in2)

    check.check_shapes(in1, in2)

    for key in in1:
        try:
            if not np.array_equal(in1[key], in2[key]):
                sys.exit(1)
                msg.error("%s datasets are different." % key)
            else:
                msg.info("%s match." % key)
        except:
            msg.warning("%s dataset too big to fit in memory. "
                        "Comparing entry by entry." % key)
            for i, val in enumerate(in1[key]):
                sys.stdout.write("Comparing %(key)s: %(progress).2f%%       \r"
                                 % {"key": key,
                                    "progress": 100.0 * i / len(in1[key])})
                sys.stdout.flush()
                if not np.array_equal(in1[key][i], in2[key][i]):
                    msg.error("Different entry (%(id) in %(key)s dataset."
                              % {"key": key, "id": i})
                    sys.exit(1)
            msg.info("%s match." % key)

    msg.info("Files are the same.")
