"""
Basic checks for data dictionaries.
"""

import sys
import msg


def get_size(data):

    """check if #entries is the same for all keys and return it

    Keyword arguments:
    data -- data dictionary
    """

    sizes = [d.shape[0] for d in data.itervalues()]  # shape[0] = #entries

    if max(sizes) != min(sizes):
        msg.error("Each dataset within a file must have the "
                  "same number of entries!")
        sys.exit(1)

    return sizes[0]


def check_keys(data1, data2):

    """Check it both files have the same datasets.

    Keyword arguments:
    data1 -- current data dictionary
    data2 -- data dictionary to be added
    """

    if data1.keys() != data2.keys():
        msg.error("Files have different datasets.")
        sys.exit(1)
