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


def build_data_dict(data1, data2, match):

    """Build a dictionary of zeros like the union of the two data
    dictionaries, but with 'length' equal to the shorter dict.
    """

    data = {}
    keys1 = [key for key in data1.keys() if key != match]
    keys2 = [key for key in data2.keys() if key != match]
    nfinal = min(np.shape(data1[match])[0],
                 np.shape(data2[match])[0])

    if nfinal == np.shape(data1[match])[0]:
        data[match] = np.zeros_like(data1[match])
    else:
        data[match] = np.zeros_like(data2[match])
    for k in keys1:
        data[k] = np.zeros_like(data1[k])
        shp = list(np.shape(data1[k]))
        shp[0] = nfinal
        data[k] = np.resize(data[k], tuple(shp))
    for k in keys2:
        data[k] = np.zeros_like(data2[k])
        shp = list(np.shape(data2[k]))
        shp[0] = nfinal
        data[k] = np.resize(data[k], tuple(shp))

    return data, keys1, keys2


def merge_data(data1, data2, match,
               print_warnings=True, show_progress=False, sorted=True):

    """Merge data1 and data2 respect to match key

    Keyword arguments:
    data1 -- dictionary with data
    data2 -- dictionary with data
    match -- common key use to order data

    if the order of the eventids (or matching idx) is sorted, we can consider:
        index2 = np.array([np.searchsorted(data2[match], i)])
    """

    data, keys1, keys2 = build_data_dict(data1, data2, match)

    # don't use enumerate here because we only want to increment the counter
    # when we have a match
    ct = 0
    for i in data1[match]:
        index1 = np.array([ct])
        index2, = np.where(data2[match] == i)
        if not index2.size:
            if print_warnings:
                msg.warning("%(key)s = %(val)d found in the first file, "
                            "but not in the second one."
                            % {"key": match, "val": i})
            continue
        data[match][ct] = i
        for key in keys1:
            data[key][ct] = data1[key][index1]
        for key in keys2:
            data[key][ct] = data2[key][index2]

        if show_progress:
            if ct % 100 == 0:
                print("finished event {}".format(ct))
        ct += 1

    # TODO - pass in a value here; generally speaking, it is not right to 
    # never allow the match index value to be zero - it might be so
    # legitimately; but for now...
    badidx = np.where(data[match] == 0)
    if len(badidx[0] > 1):
        data[match] = np.delete(data[match], badidx, axis=0)
    for key in keys1:
        data[key] = np.delete(data[key], badidx, axis=0)
    for key in keys2:
        data[key] = np.delete(data[key], badidx, axis=0)

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
