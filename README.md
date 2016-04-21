# HDF5 MANIPULATOR

Simple manipulation on hdf5 files.

## Split

Split hdf5 file:

```
usage: ./split.py <options>

HDF5 MANIPULATOR (split)

optional arguments:
  -h, --help            show this help message and exit
  --keys [key1, key2, ...]
                        list of keys to save in the output files (all if not
                        defined)
  --prefix [path/to/filename_base]
                        prefix for splitted files (base on input file if not
                        defined)
  --size [int]          number of entries per file (all entries if not
                        defined)

required arguments:
  --file [path/to/input_file]
                        path to input file to split

```

### Examples

* Simple split

  `./split.py --file /path/to/my/data/data.hdf5 --size 100`

  will create `/path/to/my/data/data_XXX.hdf5` files, each with 100 entries

* Split and extract

  `./split.py --file /path/to/my/data/data.hdf5 --size 100 --keys 'data1, data2'`

  will create `/path/to/my/data/data_XXX.hdf5` files, each with 100 entries, containing only `data1` anda `data2` datasets

* Extract subset of datasets

  `./split.py --file /path/to/my/data/data.hdf5 --keys 'data1, data2'`

  will create one file with all entries, containing only `data1` anda `data2` datasets
