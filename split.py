#!/usr/bin/env python
"""Split hdf5 file"""
import os
import sys
import h5py
import numpy as np
from parser import get_args_split as parser
import msg


def load_file(filename):

    """load hdf5 file to data dictionary and return it

    Keyword arguments:
    filename -- the full path to hdf5 file
    """

    f = h5py.File(filename, 'r')

    data = {}

    print "The following datasets were found in %s:\n" % filename

    adjust = len(max(f.keys(), key=len)) + 1  # length of left text column

    for key in f:
        data[key] = f[key][...]
        print "\t - %(key)s %(type)s %(size)s" \
            % {"key": (key+':').ljust(adjust),
               "size": '-> ' + str(data[key].shape),
               "type": ('[' + str(data[key].dtype) + ']').ljust(9),
               }

    f.close()

    return data


def get_size(data):

    """check if #entries is the same for all keys and return it

    Keyword arguments:
    data -- data dictionary
    """

    sizes = [d.shape[0] for d in data.itervalues()]  # shape[0] = #entries

    if max(sizes) != min(sizes):
        msg.error("Each dataset must have the same number of entries!")
        sys.exit(1)

    return sizes[0]


def check_keys(fkeys, ukeys):

    """check if user-requested keys are included in given hdf5 file

    Keyword arguments:
    fkeys -- keys included in a file
    ukeys -- user-requested keys
    """

    for key in ukeys:
        if key not in fkeys:
            msg.error("%s is not found in the input hdf5 file." % key)
            sys.exit(1)

    return ukeys


def create_file(prefix, i, size, data):

    """create a file with given subset of data

    Keyword arguments:
    prefix -- file prefix (path/to/base_name)
    i -- file index
    size -- number of entries
    data -- data dictionary
    """

    filename = "%(prefix)s_%(id)03d.hdf5" % {"prefix": prefix, "id": i}

    print "\t - %(file)s, with %(n)d entries" % {"file": filename, "n": size}

    f = h5py.File(filename, 'w')

    for key in data:
        # adjust dataset shape to new size
        shape = list(data[key].shape)
        shape[0] = size
        # save a subset of entries from data
        f.create_dataset(key, shape, dtype=data[key].dtype)[...] \
            = data[key][i*size:(i+1)*size]

    f.close()

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: SPLIT")

    args = parser()
    data = load_file(args.input_file)
    old_size = get_size(data)

    if args.size:
        new_size = int(args.size)
        if new_size > old_size:
            msg.error("Use splitter wisely...")
            sys.exit(1)
    else:
        new_size = old_size
        msg.info("No size given. Using size=%d" % old_size)

    nof_files, leftover = old_size / new_size, old_size % new_size

    if args.keys:
        keys = check_keys(data.keys(),
                          [k.strip() for k in args.keys.split(',')])
        print "\nThe following datasets will be saved:\n"
        for key in keys:
            print "\t - %s" % key
    else:
        keys = data.keys()
        msg.info("No user-requested keys. Saving all datasets.")

    prefix = args.prefix or os.path.splitext(args.input_file)[0]

    print "\nThe list of created files:\n"

    for i in range(nof_files):
        create_file(prefix, i, new_size, data)

    if leftover:
        create_file(prefix, nof_files, leftover, data)

    msg.info("Done")
