#!/bin/bash

# first, clean up existing HDF5s
rm -f *.hdf5

# make a set of synethic datasets in HDF5
./create_hdf5.py
./create_hdf5.py 1

# test combine.py
../combine.py --input1 matrix0.hdf5 --input2 vector0.hdf5 \
  --output matrix_vector0.hdf5 --match ids

# test combine_big.py
../combine_big.py --input1 matrix1.hdf5 --input2 vector1.hdf5 \
  --output matrix_vector1.hdf5 --match ids

# test extract.py
../extract.py --input full0.hdf5 --output matrix_number0.hdf5 \
  --keys data_matrix,data_number,ids

# test extract_big.py
../extract_big.py --input full1.hdf5 --output matrix_number1.hdf5 \
  --keys data_matrix,data_number,ids

# test merge.py -- the output will have repeating values in `ids`
../merge.py --input vector0.hdf5,vector1.hdf5 --output vector.hdf5
./print.py vector.hdf5

# test merge_big.py -- the output will have repeating values in `ids`
../merge_big.py --input matrix0.hdf5,matrix1.hdf5 --output matrix.hdf5
./print.py matrix.hdf5

# test rename_dataset.py
../rename_dataset.py --input number0.hdf5 --dataset data_number --name number
./print.py number0.hdf5

# test split.py
../split.py --input matrix0.hdf5 --size 500

# test split_big.py
../split.py --input matrix1.hdf5 --size 500

# split_big_special is special, haha, and hacky and requires inputs of a
# specific shape -- just hack the script if you want to use it.
