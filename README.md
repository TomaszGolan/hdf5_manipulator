# HDF5 MANIPULATOR

Simple manipulation on hdf5 files.

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

## Merge

Merge hdf5 files (requires the same datasets in all input files):

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

TODO: Save different datasets from different files into one output hdf5

## Test: create_hdf5.py

Create several hdf5 files filled with random numbers, matrices etc.

## Test: diff.py

Check if two hdf5 files are exactly the same.
