#!/bin/bash

PYEXEC="merge_big.py"

SAMPLE=minerva1nofsimc

# note
#  python fuelme.py $OUT 0.83 0.10
# was the "historic standard", but switching as of me1Amc energy+time lattice

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_${SAMPLE}_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_${SAMPLE}.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_${SAMPLE}_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_${SAMPLE}.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07

