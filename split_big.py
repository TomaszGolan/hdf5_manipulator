#!/usr/bin/env python
"""
Split hdf5 (big) file
"""
import os
import sys
from collections import OrderedDict
from parser import get_args_split as parser
import msg
import hdf5
import h5py
import check
from combine_big import load
from split import generate_filelist
from split import save_filelist

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: SPLIT")

    args = parser()

    data = load(args.input)

    filelist = generate_filelist(
        args.prefix or os.path.splitext(args.input)[0],
        check.get_size(data), int(args.size))

    print "\nSaving output files:\n"

    for f, r in filelist.iteritems():
        msg.list_fileinfo(f, r)
        hdf5.save_subset_big(f, data, r[0], r[1])

    if args.filelist:
        save_filelist(args.filelist, filelist.keys())

    data.close()

    msg.info("Done")
