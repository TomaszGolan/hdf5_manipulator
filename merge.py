#!/usr/bin/env python
"""
Merge hdf5 files
"""
import os
import sys
import hdf5
import numpy as np
from collections import OrderedDict
from parser import get_args_merge as parser
import msg
import check


def get_filelist(bases):

    """look for files which match given bases and return them as list

    Keyword arguments:
    bases -- list of 'path/basename'
    """

    filelist = []

    for base in bases:
        path, fname = os.path.dirname(base) or '.', os.path.basename(base)
        filelist.extend([path + '/' + f for f in os.listdir(path)
                        if f.startswith(fname) and f.endswith(".hdf5")])

    return sorted(filelist)


def merge_data(data_list):

    """Merge dictionaries with data.

    Keyword arguments:
    data_list -- the dictionary with data dictionaries
    """

    data = None

    for f in data_list:
        size = check.get_size(data_list[f])
        if not data:
            print "\nThe following datasets were found in %s:\n" % f
            msg.list_dataset(data_list[f])
            data = data_list[f]
        else:
            print "\nAdding %(n)d entries from %(f)s" % {"n": size, "f": f}
            check.check_keys(data, data_list[f])
            check.check_shapes(data, data_list[f])
            for key in data_list[f]:
                data[key] = np.append(data[key], data_list[f][key], axis=0)

    return data

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: MERGE")

    args = parser()

    filelist = get_filelist([f.strip() for f in args.input_files.split(',')])

    if not filelist:
        msg.error("No files matching --input were found.")
        sys.exit(1)

    print "The following input files were found:\n"

    for f in filelist:
        print "\t - %s" % f

    data = OrderedDict()

    for f in filelist:
        data[f] = hdf5.load(f)

    hdf5.save(args.output, merge_data(data))

    msg.info("Done")
