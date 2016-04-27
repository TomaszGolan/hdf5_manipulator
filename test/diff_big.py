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


def fullcheck(data1, data2, key):

    """Do full comparison entry by entry.

    Keyword arguments:
    data1 -- numpy array with data
    data2 -- numpy array with data
    key -- dataset being checked
    """

    msg.warning("%s dataset too big to fit in memory. "
                "Comparing entry by entry." % key)
    for i, val in enumerate(data1):
        sys.stdout.write("Comparing %(key)s: %(progress).2f%%       \r"
                         % {"key": key,
                            "progress": 100.0 * i / len(data1)})
        sys.stdout.flush()
        if not np.array_equal(data1[i], data2[i]):
            msg.error("Different entry %(id)d in %(key)s dataset."
                      % {"key": key, "id": i})
            sys.exit(1)


def partcheck(data1, data2, key, n=100):

    """Do full comparison entry by entry.

    Keyword arguments:
    data1 -- numpy array with data
    data2 -- numpy array with data
    key -- dataset being checked
    n -- number of entries to compare in each part of the file
    """

    msg.warning("%(key)s dataset too big to fit in memory. "
                "Comparing first / last / random %(n)d entries."
                % {"key": key, "n": n})

    N = len(data1)
    entries = range(n)
    entries.extend(range(N-n, N))
    entries.extend(np.random.randint(low=n, high=N-n, size=n))

    for i in entries:
        if not np.array_equal(data1[i], data2[i]):
            msg.error("Different entry %(id)d in %(key)s dataset."
                      % {"key": key, "id": i})
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: ./diff file1 file2 [fullcheck]"
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
            if len(sys.argv) == 4 and sys.argv[3] == "fullcheck":
                fullcheck(in1[key], in2[key], key)
            else:
                partcheck(in1[key], in2[key], key)

            msg.info("%s match." % key)

    in1.close()
    in2.close()

    msg.info("Files are the same.")
