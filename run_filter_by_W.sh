#!/bin/bash

INP="minosmatch_nukecczdefs_genallz_pcodecap66_kinedat_127x50x25_xuv_me1Bmc.hdf5"

OUT="minosmatch_nukecczdefs_genallz_pcodecap66_kinedat_127x50x25_xuv_me1Bmc_lowW.hdf5"
WMIN=0.0
WMAX=2000.0
cat << EOF
python filter_by_W.py -i $INP -o $OUT \
  --train_frac 0.86 --valid_frac 0.07 \
  --wmin $WMIN --wmax $WMAX
EOF
python filter_by_W.py -i $INP -o $OUT \
  --train_frac 0.86 --valid_frac 0.07 \
  --wmin $WMIN --wmax $WMAX

OUT="minosmatch_nukecczdefs_genallz_pcodecap66_kinedat_127x50x25_xuv_me1Bmc_highW.hdf5"
WMIN=2000.0
WMAX=9999999.0
cat << EOF
python filter_by_W.py -i $INP -o $OUT \
  --train_frac 0.86 --valid_frac 0.07 \
  --wmin $WMIN --wmax $WMAX
EOF
python filter_by_W.py -i $INP -o $OUT \
  --train_frac 0.86 --valid_frac 0.07 \
  --wmin $WMIN --wmax $WMAX

