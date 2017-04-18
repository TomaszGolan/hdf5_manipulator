#!/usr/bin/env python
"""
build new hdf5 file based on filtering by value
"""
from __future__ import print_function
import os
import numpy as np
import h5py
from fuel.datasets.hdf5 import H5PYDataset


def get_filtered_idx(hdf5file, Wmin=2000.0, Wmax=2500.0):
    idx1 = hdf5file['W'][:] >= Wmin
    idx2 = hdf5file['W'][:] < Wmax
    idx = np.where(idx1 & idx2)
    return list(idx[0])


def get_num_evts(hdf5file):
    return np.shape(hdf5file[hdf5file.keys()[0]])[0]


def slices_maker(n, slice_size):
    if n < slice_size:
        return [(0, n)]

    remainder = n % slice_size
    n = n - remainder
    nblocks = n // slice_size
    counter = 0
    slices = []
    for i in range(nblocks):
        end = counter + slice_size
        slices.append((counter, end))
        counter += slice_size

    if remainder != 0:
        slices.append((counter, counter + remainder))

    return slices


def create_datasets(inp, outp, idx, slice_size):
    slices = slices_maker(len(idx), slice_size)
    for key in inp.keys():
        shp = list(inp[key].shape)
        shp[0] = len(idx)
        outp.create_dataset(
            key, shp, dtype=inp[key].dtype, compression='gzip'
        )
        first_idx = 0
        last_idx = 0
        for s in slices:
            print('... filtering events {} to {} for {}'.format(
                s[0], s[1], key
            ))
            temp_idx = idx[s[0]: s[1]]
            nentries = len(temp_idx)
            last_idx += nentries
            print('... -> copying events into new indices {} to {}'.format(
                first_idx, last_idx
            ))
            outp[key][first_idx: last_idx] = inp[key][temp_idx]
            first_idx += nentries


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage=__doc__)
    parser.add_option('-i', '--input_file', dest='input_file',
                      default='./in.hdf5',
                      help='Input file name',
                      metavar='INPUT_FILE_NAME')
    parser.add_option('-o', '--output_file', dest='output_file',
                      default='./out.hdf5',
                      help='Output file name',
                      metavar='OUTPUT_FILE_NAME')
    parser.add_option('-s', '--slice_size', dest='slice_size',
                      default=100000, type='int',
                      help='Chunk size for copying',
                      metavar='SLICE_SIZE')
    parser.add_option('-t', '--train_frac', dest='train_frac',
                      default=0.86, type='float',
                      help='Training fraction',
                      metavar='TRAIN_FRAC')
    parser.add_option('-v', '--valid_frac', dest='valid_frac',
                      default=0.07, type='float',
                      help='Validation fraction',
                      metavar='VALID_FRAC')
    parser.add_option('--wmin', dest='wmin',
                      default=0.0, type='float',
                      help='min W',
                      metavar='W_MIN')
    parser.add_option('--wmax', dest='wmax',
                      default=2000.0, type='float',
                      help='max W',
                      metavar='W_MAX')
    (options, args) = parser.parse_args()

    train_frac = options.train_frac
    valid_frac = options.valid_frac

    input_file = h5py.File(options.input_file, 'r')
    if os.path.exists(options.output_file):
        os.remove(options.output_file)
    output_file = h5py.File(options.output_file, 'w')

    idx = get_filtered_idx(input_file, Wmin=options.wmin, Wmax=options.wmax)
    create_datasets(
        input_file, output_file, idx, slice_size=options.slice_size
    )

    num_evts = get_num_evts(output_file)
    n_train = int(train_frac * num_evts)
    n_valid = int(valid_frac * num_evts)
    n_test = num_evts - n_train - n_valid

    train_dict = {name: (0, n_train)
                  for name in output_file.keys()}
    valid_dict = {name: (n_train, n_train + n_valid)
                  for name in output_file.keys()}
    test_dict = {name: (n_train + n_valid, num_evts)
                 for name in output_file.keys()}

    split_dict = {
        'train': train_dict,
        'valid': valid_dict,
        'test': test_dict
    }

    output_file.attrs['split'] = H5PYDataset.create_split_array(split_dict)

    output_file.close()
    input_file.close()
