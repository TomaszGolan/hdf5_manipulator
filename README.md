# HDF5 MANIPULATOR

Simple manipulation on hdf5 files.

*Note: for files too big to fit in memory, use *_big.py*

## Split

Split hdf5 file (requires the same no. of entries per dataset):

```
usage: ./split.py <options>

HDF5 MANIPULATOR (split)

optional arguments:
  -h, --help            show this help message and exit
  --prefix [path/to/filename_base]
                        prefix for splitted files (base on input file if not
                        defined)
  --filelist [path/to/filelist]
                        save output files list in txt file

required arguments:
  --input [path/to/input_file]
                        path to input hdf5 file
  --size [int]          number of entries per file
```

* Example:

  `./split.py --input /path/to/my/data/data.hdf5 --size 100`

  will create `/path/to/my/data/data_XXX.hdf5` files, each with 100 entries
  (the last one may have less no. of entries)

## Merge

Merge hdf5 files (requires the same datasets, with the same shapes,
in all input files):

```
usage: ./merge.py <options>

HDF5 MANIPULATOR (merge)

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  --input [list of input files]
                        path to input hdf5 files to merge ('file1, file2,...'
                        will look for all files starts with file1 and file2
                        and ends with .hdf5)
  --output [path/to/filename]
                        path to output hdf5 file
```

* Example:

  `./merge.py --input '/path1/basename1, /path2/basename2' --output merged.hdf5`

  will merge all files matching `/path1/basename1*` and `/path2/basename2*`
  into `merged.hdf5` file

## Extract

Extract chosen datasets from hdf5 file (requires the same no. of entries
per dataset):

```
usage: ./extract.py <options>

HDF5 MANIPULATOR (extract)

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  --input [path/to/filename]
                        path to input hdf5 file
  --output [path/to/filename]
                        path to output hdf5 file
  --keys ['key1, key2, ...']
                        list of datasets to be saved in the output file
```

* Example:

  `./extract.py --input /path/to/input.hdf5 --output /path/to/output.hdf5 --keys 'dataset1, dataset2'`

  will extract `dataset1` and `dataset2` from `input.hdf5`
  and save in `output.hdf5`

## Combine

Save different datasets from different files into one output hdf5
(requires the same no. of entries per dataset within the file
and one common key use for ordering):

```
usage: ./combine.py <options>

HDF5 MANIPULATOR (combine)

optional arguments:
  -h, --help            show this help message and exit
  --keys1 ['key1, key2, ...']
                        list of datasets to be extracted from the first input
                        file (use all if not defined)
  --keys2 ['key1, key2, ...']
                        list of datasets to be extracted from the second input
                        file (use all if not defined)

required arguments:
  --input1 [path/to/filename1]
                        path to first input hdf5 file
  --input2 [path/to/filename2]
                        path to second input hdf5 file
  --output [path/to/filename]
                        path to output hdf5 file
  --match [key]         the common key use to order data
```

* Example 1:

  `./combine.py --input1 /path/to/file1 --input2 /path/to/file2 --output /path/to/output --match id`

  requires both input files have `id` key, and no other common keys;
  will create a file which contains all datasets from input files
  for all entries with matching `id`s

* Example 2:

  `./combine.py --input1 /path/to/file1 --input2 /path/to/file2 --output /path/to/output --match id --keys1 'data1' --keys2 'data2, data3'`

  will create a file which contains `data1` from `file1`, `data2` and `data3`
  from `file2` (for all entries with matching `ids`s)

## Test: create_hdf5.py

Create several hdf5 files filled with random numbers, matrices etc.

## Test: diff.py

Check if two hdf5 files are exactly the same.

## Test: diff_big.py

Check if two hdf5 files are exactly the same. If single dataset is too big to
fit into memory it can perform partial check [default] or full check.

* Example 1:

  `./diff_big.py file1 file2`

  if some dataset is too big, it will check first 100 entries, last 100 entries, and random 100 entries.

* Example 2:

  `./diff_big.py file1 file2 fullcheck`

  if some dataset is too big, it will check dataset entry
  by entry (takes a lot of time).
