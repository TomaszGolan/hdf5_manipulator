"""
Command line parser for HDF5 MANIPULATOR
"""

import argparse


def get_args_split():

    """parse arguments for split"""

    parser = argparse.ArgumentParser(
        description="HDF5 MANIPULATOR (split)",
        usage="./split.py <options>"
        )

    parser.add_argument(
        "--keys", action="store", dest="keys", metavar="[key1, key2, ...]",
        default=None,
        help="list of keys to save in the output files (all if not defined)"
        )

    parser.add_argument(
        "--prefix", action="store", dest="prefix",
        metavar="[path/to/filename_base]", default=None,
        help="prefix for splitted files (base on input file if not defined)"
        )

    parser.add_argument(
        "--size", action="store", dest="size", metavar="[int]", default=None,
        help="number of entries per file (all entries if not defined)"
    )

    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "--file", action="store", dest="input_file",
        metavar="[path/to/input_file]", required=True,
        help="path to input file to split"
    )

    return parser.parse_args()
