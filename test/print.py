#!/usr/bin/env python
"""
Print info on datasets in hdf5 file.
"""
import sys
sys.path.append('..')
import hdf5
import msg


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: ./print file")
        sys.exit(1)

    print("\nThe following datasets were found in %s:\n" % sys.argv[1])
    msg.list_dataset(hdf5.load(sys.argv[1]))
