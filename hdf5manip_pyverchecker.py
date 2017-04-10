#!/usr/bin/env python
from __future__ import print_function

import sys
import importlib

print('Python version: {}'.format(sys.version))

def test_module_version(module_name):
    try:
        mod = importlib.import_module(module_name)
        print('{} version: {}'.format(module_name, mod.__version__))
    except ImportError:
        print('Missing {}'.format(module_name))
    except Exception as e:
        print(e)

modules = [
    'h5py', 'fuel', 'numpy', 'argparse',
]

for mod in modules:
    test_module_version(mod)
