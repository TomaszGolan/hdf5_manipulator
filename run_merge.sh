#!/bin/bash

PYEXEC="merge_big.py"
SAMPLE=me1Bmc

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_me1Bmc_pt1_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_me1Bmc.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.83 0.10
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.83 0.10

