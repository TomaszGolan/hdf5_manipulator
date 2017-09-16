#!/usr/bin/env python
from __future__ import print_function

import os
from collections import OrderedDict

import numpy as np
import h5py

from MnvReaderSQLite import MnvCategoricalSQLiteReader

HDF5B = '/data/perdue/minerva/hdf5/201700'
DBB = '/data/perdue/minerva/dbs'
# HDF5B = '.'
# DBB = '.'

DBBASE = DBB + '/' + 'prediction67_me1Amc_epsilon1480703388'
KINEFILE = HDF5B + '/' + 'minosmatch_kinedat_me1Amc.hdf5'
ZACTUALFLE = HDF5B + '/' + 'me1Amc_zpluskine.hdf5'
# OUTFILE = HDF5B + '/' + 'me1Amc_zzpredpluskine.hdf5'
OUTBASE = HDF5B + '/' + 'me1Amc_zzpredpluskine'


def prepare_hdf5_file(hdf5file):
    if os.path.exists(hdf5file):
        os.remove(hdf5file)
    f = h5py.File(hdf5file, 'w')
    return f


def build_dset_description():
    dset_description = OrderedDict(
        (('planecodes_pred', ('uint16', 'plane-id-code-pred')),
         ('planecodes_actual', ('uint16', 'plane-id-code-actual')),
         ('current', ('uint8', 'current')),
         ('int_type', ('uint8', 'int_type')),
         ('W', ('float32', 'W')),
         ('Q2', ('float32', 'Q2')),
         ('nuE', ('float32', 'nuE')),
         ('lepE', ('float32', 'lepE')),
         ('xbj', ('float32', 'xbj')),
         ('ybj', ('float32', 'ybj')),
         ('targZ', ('uint8', 'targZ')),
         ('eventids', ('uint64', 'run+subrun+gate+slices[0]')))
    )
    return dset_description


def create_1d_dset(hdf5file, name, dtype, label):
    data_set = hdf5file.create_dataset(name, (0,),
                                       dtype=dtype, compression='gzip',
                                       maxshape=(None,))
    data_set.dims[0].label = label


def prep_datasets_using_dset_descrip_only(hdf5file, dset_description):
    """
    hdf5file - where we will add dsets,
    dset_desciption - ordered dict containing all the pieces of the dset
    """
    dset_names = dset_description.keys()
    for dset_name in dset_names:
        create_1d_dset(hdf5file,
                       dset_name,
                       dset_description[dset_name][0],
                       dset_description[dset_name][1])


def decode_eventid(eventid):
    """
    assume "standard" encoding
    """
    evtid = str(eventid)
    phys_evt = int(evtid[-2:])
    evtid = evtid[:-2]
    gate = int(evtid[-4:])
    evtid = evtid[:-4]
    subrun = int(evtid[-4:])
    evtid = evtid[:-4]
    run = int(evtid)
    return (run, subrun, gate, phys_evt)


def make_example_container(dset_description):
    example_container = {}
    for k in dset_description.keys():
        example_container[k] = -1
    return example_container


def process_block(filenum, start, stop):
    reader = MnvCategoricalSQLiteReader(67, DBBASE)
    kine_d = h5py.File(KINEFILE, 'r')
    z_act = h5py.File(ZACTUALFLE, 'r')

    output_file = OUTBASE + '{:08d}'.format(filenum) + '.hdf5'
    f = prepare_hdf5_file(output_file)
    dset_description = build_dset_description()
    prep_datasets_using_dset_descrip_only(f, dset_description)
    example_container = make_example_container(dset_description)

    for i, evt in enumerate(z_act['eventids'][start:stop]):
        example_container['eventids'] = evt
        r, s, g, p = decode_eventid(evt)
        # get the acutal value
        example_container['planecodes_actual'] = \
            z_act['planecodes'][i + start]
        # get the predicted value
        try:
            example_container['planecodes_pred'] = \
                reader.get_argmax_prediction(r, s, g, p)
        except:
            example_container['planecodes_pred'] = 0
        if example_container['planecodes_pred'] == 0:
            # don't have predictions for this
            continue
        # get the kinematics values
        idx = np.where(
            kine_d['eventids'][:] == example_container['eventids']
        )
        if idx[0].shape[0] == 0:
            # don't have the kin values for this
            continue
        else:
            idx = idx[0][0]
        example_container['Q2'] = kine_d['Q2'][idx]
        example_container['W'] = kine_d['W'][idx]
        example_container['current'] = kine_d['current'][idx]
        example_container['eventids'] = kine_d['eventids'][idx]
        example_container['int_type'] = kine_d['int_type'][idx]
        example_container['lepE'] = kine_d['lepE'][idx]
        example_container['nuE'] = kine_d['nuE'][idx]
        example_container['targZ'] = kine_d['targZ'][idx]
        example_container['xbj'] = kine_d['xbj'][idx]
        example_container['ybj'] = kine_d['ybj'][idx]
        # write to hdf5
        existing_examples = np.shape(f['eventids'])[0]
        total_examples = existing_examples + 1
        for k in example_container.keys():
            f[k].resize(total_examples, axis=0)
            f[k][existing_examples] = example_container[k]

    kine_d.close()
    z_act.close()
    f.close()


def slices_maker(n, slice_size=100000):
    """
    make "slices" of size `slice_size` from a file of `n` events
    (so, [0, slice_size), [slice_size, 2 * slice_size), etc.)
    """
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


if __name__ == '__main__':

    z_act = h5py.File(ZACTUALFLE, 'r')
    num_b = np.shape(z_act['eventids'])[0]
    slcs = slices_maker(num_b, 10000)
    for i, s in enumerate(slcs[0:]):
        if i < 0:
            continue
        process_block(i, s[0], s[1])
