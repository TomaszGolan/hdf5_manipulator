#!/bin/bash

PYEXEC="merge_big.py"

SAMPLE=me1Adata

# INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_vtxinfo_${SAMPLE}_"
# OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_vtxinfo_${SAMPLE}.hdf5"
# cat << EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10
# EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10

# INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_${SAMPLE}_"
# OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_${SAMPLE}.hdf5"
# cat << EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10
# EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10

# INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_muondat_${SAMPLE}_"
# OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_muondat_${SAMPLE}.hdf5"
# cat << EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10
# EOF
# python $PYEXEC --input $INP --output $OUT
# python fuelme.py $OUT 0.83 0.10

SAMPLE=minerva13Bmc

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_${SAMPLE}_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_${SAMPLE}.hdf5"
cat << EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.83 0.10
EOF
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUT 0.83 0.10

