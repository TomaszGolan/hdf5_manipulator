#!/usr/bin/env python
"""
Combine different datasets from two hdf5 files
"""
import hdf5
import numpy as np
from parser import get_args_combine as parser
import msg
import check
from extract import update_data


def add(data, key, value):

    """Add element to data[key]. Crete new key if necessary.

    Keyword arguments:
    data -- dictionary to update_data
    key -- key to update_data
    value -- value to be added
    """

    if key not in data.keys():
        data[key] = value
    else:
        data[key] = np.append(data[key], value, axis=0)


def merge_data(data1, data2, match, print_warnings=True, show_progress=False):

    """Merge data1 and data2 respect to match key

    Keyword arguments:
    data1 -- dictionary with data
    data2 -- dictionary with data
    match -- common key use to order data
    """

    data = {}
    keys1 = [key for key in data1.keys() if key != match]
    keys2 = [key for key in data2.keys() if key != match]

    for ct, i in enumerate(data1[match]):
        index1 = np.array([ct])
        index2, = np.where(data2[match] == i)
        if not index2.size:
            if print_warnings:
                msg.warning("%(key)s = %(val)d found in the first file, "
                            "but not in the second one."
                            % {"key": match, "val": i})
            continue
        add(data, match, [i])
        for key in keys1:
            add(data, key, data1[key][index1])
        for key in keys2:
            add(data, key, data2[key][index2])

        if show_progress:
            if ct % 100 == 0:
                print("finished event {}".format(ct))

    return data


def get_data(filename, match, keys):

    """Load file, check if contains match,
    update datasets based on command line options. Return data dictionary.

    Keyword arguments:
    filename -- input hdf5 file
    match -- common key use to order data
    keys -- user-chosen datasets to save
    """

    data = hdf5.load(filename)

    print "\nThe following datasets were found in %s:\n" % filename
    msg.list_dataset(data)

    check.key_exists(match, data, filename)

    if keys:
        msg.info("Using only: " + keys)
        update_data(data, [k.strip() for k in keys.split(',')], args.match)

    return data

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: COMBINE")

    args = parser()

    data1 = get_data(args.input1, args.match, args.keys1)
    data2 = get_data(args.input2, args.match, args.keys2)

    check.different_keys(data1, data2, args.match)

    data = merge_data(data1, data2, args.match,
                      args.print_warnings, args.show_progress)

    print "\nThe following datasets will be saved in %s:\n" % args.output
    msg.list_dataset(data)

    hdf5.save(args.output, data)

    msg.info("Done")
