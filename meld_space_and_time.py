#!/usr/bin/env python
"""
build new hdf5 file with pulse height and time tensors combined
"""
from __future__ import print_function
import os
import numpy as np
import h5py
from fuel.datasets.hdf5 import H5PYDataset


def get_num_evts(hdf5file):
    return np.shape(hdf5file[hdf5file.keys()[0]])[0]


def slices_maker(n, slice_size=100000):
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


def create_other_datasets(outp, inp, ks):
    slices = slices_maker(get_num_evts(inp))
    for key in ks:
        shp = list(inp[key].shape)
        outp.create_dataset(
            key, shp, dtype=inp[key].dtype, compression='gzip'
        )
        for s in slices:
            print('... copying events {} to {} for {}'.format(
                s[0], s[1], key
            ))
            outp[key][s[0]: s[1]] = inp[key][s[0]: s[1]]


def create_melded_datasets(outp, inp):
    """
    merge the time and pulse height tensors
    """
    slices = slices_maker(get_num_evts(inp))
    for p, t in zip(['hits-u', 'hits-v', 'hits-x'],
                    ['times-u', 'times-v', 'times-x']):
        shp = list(inp[p].shape)  # [n-evt, 1, h, w]
        shp[1] = 2
        new_name = 'hitimes-' + p.split('-')[1]
        outp.create_dataset(
            new_name, shp, dtype=inp[p].dtype, compression='gzip'
        )
        for s in slices:
            print('... merging events {} to {} for {}'.format(
                s[0], s[1], new_name
            ))
            outp[new_name][s[0]: s[1], 0, :, :] = inp[p][s[0]: s[1], 0, :, :]
            outp[new_name][s[0]: s[1], 1, :, :] = inp[t][s[0]: s[1], 0, :, :]


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
                      default=0.83, type='float',
                      help='Training fraction',
                      metavar='TRAIN_FRAC')
    parser.add_option('-v', '--valid_frac', dest='valid_frac',
                      default=0.1, type='float',
                      help='Validation fraction',
                      metavar='VALID_FRAC')
    (options, args) = parser.parse_args()

    train_frac = options.train_frac
    valid_frac = options.valid_frac

    # `f` is input, `g` is output...
    f = h5py.File(options.input_file, 'r')
    if os.path.exists(options.output_file):
        os.remove(options.output_file)
    g = h5py.File(options.output_file, 'w')

    tkeys = f.keys()
    for k in ['hits-u', 'hits-v', 'hits-x', 'times-u', 'times-v', 'times-x']:
        tkeys.remove(k)

    create_other_datasets(g, f, tkeys)
    create_melded_datasets(g, f)

    num_evts = get_num_evts(f)
    n_train = int(train_frac * num_evts)
    n_valid = int(valid_frac * num_evts)
    n_test = num_evts - n_train - n_valid

    train_dict = {name: (0, n_train)
                  for name in g.keys()}
    valid_dict = {name: (n_train, n_train + n_valid)
                  for name in g.keys()}
    test_dict = {name: (n_train + n_valid, num_evts)
                 for name in g.keys()}

    split_dict = {
        'train': train_dict,
        'valid': valid_dict,
        'test': test_dict
    }

    g.attrs['split'] = H5PYDataset.create_split_array(split_dict)

    g.close()
