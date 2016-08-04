#!/bin/bash

PYEXEC="merge_big.py"

# SAMPLE=me1Bmc
# INP="minosmatch_muondat_${SAMPLE}_"
# OUT="minosmatch_muondat_${SAMPLE}.hdf5"
# python $PYEXEC --input $INP --output $OUT
#
# INP="minosmatch_singlepi0_${SAMPLE}_"
# OUT="minosmatch_singlepi0_${SAMPLE}.hdf5"
# python $PYEXEC --input $INP --output $OUT
#
# INP="minosmatch_singlepi0_tracker_127x72x36_${SAMPLE}_"
# OUT="minosmatch_singlepi0_tracker_127x72x36_xuv_${SAMPLE}.hdf5"
# python $PYEXEC --input $INP --output $OUT

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_vtxinfo_me1Bmc_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_vtxinfo_me1Bmc.hdf5"
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUTP 0.83 0.10

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_me1Bmc_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_me1Bmc.hdf5"
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUTP 0.83 0.10

INP="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_muondat_me1Bmc_"
OUT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_muondat_me1Bmc.hdf5"
python $PYEXEC --input $INP --output $OUT
python fuelme.py $OUTP 0.83 0.10

