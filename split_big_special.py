#!/usr/bin/env python
"""
Split hdf5 (big) file into non-equal chunks
"""
import os
from parser import get_args_split as parser
import msg
import hdf5
import check
from combine_big import load
from split import generate_uneven_filelist
from split import save_filelist

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: SPLIT")

    args = parser()

    data = load(args.input)

    # TODO - come up with a clever way to generalize this...
    new_sizes = [(0, 50000), (50000, 60000), (60000, 70000)]
    new_names = ['mnist_train.hdf5', 'mnist_valid.hdf5', 'mnist_test.hdf5']
    new_filelist = zip(new_names, new_sizes)

    filelist = generate_uneven_filelist(
        args.prefix or os.path.splitext(args.input)[0],
        check.get_size(data),
        new_filelist
    )

    print "\nSaving output files:\n"

    for f, r in filelist.iteritems():
        msg.list_fileinfo(f, r)
        hdf5.save_subset_big(f, data, r[0], r[1])

    if args.filelist:
        save_filelist(args.filelist, filelist.keys())

    data.close()

    msg.info("Done")
