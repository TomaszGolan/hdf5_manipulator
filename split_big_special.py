#!/usr/bin/env python
"""
Split hdf5 (big) file into non-equal chunks
"""
import os
from parser import get_args_split as parser
import msg
import hdf5
from combine_big import load
from split import generate_uneven_filelist
from split import save_filelist

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: SPLIT")

    args = parser()

    data = load(args.input)

    # TODO - come up with a clever way to generalize this...
    new_sizes = [(0, 15000), (15000, 17500), (17500, 20000)]
    new_names_ext = ['_train.hdf5', '_valid.hdf5', '_test.hdf5']
    new_filelist = zip(new_names_ext, new_sizes)

    filelist = generate_uneven_filelist(
        args.prefix or os.path.splitext(args.input)[0],
        new_filelist
    )

    print("\nSaving output files:\n")

    for f, r in filelist.iteritems():
        msg.list_fileinfo(f, r)
        hdf5.save_subset_big(f, data, r[0], r[1])

    if args.filelist:
        save_filelist(args.filelist, filelist.keys())

    data.close()

    msg.info("Done")
