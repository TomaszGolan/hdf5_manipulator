#!/usr/bin/env python
"""
Combine different datasets from two (big) hdf5 files
"""
import os
import sys
import h5py
import numpy as np
from collections import OrderedDict
from parser import get_args_combine as parser
import msg
import check
from extract import update_data


def match(input1, input2, output, key):

    """Check if matching dataset is the same for inputs. Copy to output.

    input1 -- input file
    input2 -- input file
    output -- output file
    key -- dataset to match
    """

    if key not in input1 or key not in input2:
        msg.error("Both files must contains %s" % key)
        sys.exit(1)

    if len(input1[key].shape) != 1 or len(input2[key].shape) != 1:
        msg.error("Matching key should have (N,) shape.")
        sys.exit(1)

    if not np.array_equal(input1[key], input2[key]):
        msg.error("%s in input files are not the same." % key)
        sys.exit(1)

    msg.info("Copying %s" % key)

    input1.copy(key, output)


def get_keys(source, keys, skip):

    """Compare user-requested keys with datasets in source file.
    Return keys to copy.

    Keyword arguments:
    source -- input file
    keys -- user-requested keys
    skip -- matching dataset already copied
    """

    if not keys:
        keys = source.keys()
    else:
        keys = [k.strip() for k in keys.split(',')]
        for k in keys:
            if k not in source.keys():
                keys.remove(k)
                msg.warning("%s requested, but not found." % k)

    if skip in keys:
        keys.remove(skip)

    return keys


def copy(source, output, keys):

    """Copy selected datasets.

    Keyword arguments:
    source -- input file
    output -- output file
    keys -- datasets to be copied
    """

    for k in keys:
        msg.info("Copying %s" % k)
        source.copy(k, output)


def load(filename, mode='r'):

    """Load hdf5 file and print included datasets.

    Keyword arguments:
    filename -- file to load
    """

    f = h5py.File(filename, mode)

    print "\nThe following datasets were found in %s:\n" % filename
    msg.list_dataset(f)

    return f

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: COMBINE")

    args = parser()

    in1, in2 = load(args.input1), load(args.input2)

    out = h5py.File(args.output, 'w')

    match(in1, in2, out, args.match)

    check.same_sizes(in1, in2)

    keys1 = get_keys(in1, args.keys1, args.match)
    keys2 = get_keys(in2, args.keys2, args.match)

    check.check_duplicates(keys1, keys2)

    copy(in1, out, keys1)
    copy(in2, out, keys2)

    print "\nThe following datasets were saved in %s:\n" % args.output
    msg.list_dataset(out)

    in1.close()
    in2.close()
    out.close()

    msg.info("Done")
