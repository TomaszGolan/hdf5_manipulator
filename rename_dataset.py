#!/usr/bin/env python
"""
Rename dataset
"""
import os
import sys
import h5py
from parser import get_args_rename as parser
from combine_big import load
import msg

if __name__ == '__main__':

    msg.box("HDF5 MANIPULATOR: COMBINE")

    args = parser()

    f = load(args.input, 'r+')

    if args.dataset not in f:
        msg.error("There is no %(key)s in %(file)s."
                  % {"key": args.dataset, "file": args.input})
        sys.exit(1)

    if args.name in f:
        msg.error("There is %(key)s already in %(file)s."
                  % {"key": args.name, "file": args.input})
        sys.exit(1)

    f[args.name] = f[args.dataset]
    del f[args.dataset]

    f.close()

    msg.info("Done")
