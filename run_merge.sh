#!/bin/bash

PYEXEC="merge_big.py"

# note
#  python fuelme.py $OUT 0.83 0.10
# was the "historic standard", but switching as of me1Amc energy+time lattice

INP="minosmatch_nukecczdefs_genallz_pcodecap66_kinedat_127x50x25_xuv_me1Bmc_"
OUT="minosmatch_nukecczdefs_genallz_pcodecap66_kinedat_127x50x25_xuv_me1Bmc.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07

