#!/usr/bin/env python
"""
Create hdf5 file with a subset of datasets from original hdf5 file
"""
import os
import sys
import hdf5
import numpy as np
from parser import get_args_extract as parser
import msg
import check


def update_data(data, keys, skip=None):

    """Remove not requested datasets.

    Keyword arguments:
    data -- dicionary with data
    keys -- user-requested keys
    skip -- the key not to delete
    """

    for key in data.keys():
        if key == skip:
            continue
        if key not in keys:
            del data[key]

    if not len(data):
        msg.error("No datasets to process.")
        sys.exit(1)

    check.get_size(data)

    for key in keys:
        if key not in data.keys():
            msg.warning("%s requested, but not found." % key)

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: EXTRACT")

    args = parser()
    data = hdf5.load(args.input)

    print "The following datasets were found in %s:\n" % args.input
    msg.list_dataset(data)

    update_data(data, [k.strip() for k in args.keys.split(',')])

    print "\nThe following dataset will be saved in %s:\n" % args.output
    msg.list_dataset(data)

    hdf5.save(args.output, data)

    msg.info("Done")
