#!/bin/bash

PYEXEC="merge_big.py"

# SAMPLE=minerva1nofsimc

# note
#  python fuelme.py $OUT 0.83 0.10
# was the "historic standard", but switching as of me1Amc energy+time lattice

INP="minosmatch_kinedat_me1Bmc_"
OUT="minosmatch_kinedat_me1Bmc.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07

