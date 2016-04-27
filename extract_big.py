#!/usr/bin/env python
"""
Create hdf5 file with a subset of datasets from original (big) hdf5 file
"""
import os
import sys
import h5py
import numpy as np
from parser import get_args_extract as parser
import msg
import check


def copy(source, output, keys):

    """Copy requested datasets.

    Keyword arguments:
    source -- input file
    output -- output file
    keys -- keys to be copied
    """

    for k in keys:
        if k not in source:
            msg.warning("%s requested, but not found." % k)
            continue
        else:
            msg.info("Copying %s" % k)
            source.copy(k, output)


if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: EXTRACT")

    args = parser()
    f = h5py.File(args.input, 'r')
    o = h5py.File(args.output, 'w')

    print "The following datasets were found in %s:\n" % args.input
    msg.list_dataset(f)

    copy(f, o, [k.strip() for k in args.keys.split(',')])

    if len(o):
        print "\nThe following dataset were saved in %s:\n" % args.output
        msg.list_dataset(o)
    else:
        msg.warning("No datasets were copied.")

    f.close()
    o.close()

    msg.info("Done")
