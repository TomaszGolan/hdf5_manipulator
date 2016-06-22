#!/bin/bash

# keys should include n-hadmultmeas instead of i-signal
# INP1="minosmatch_hadmult_me1Bmc.hdf5"
# INP2="minosmatch_nukecczdefs_127x94x47_me1Bmc.hdf5"
# OUTP="minosmatch_hadmult_127x94x47_xuv_me1Bmc.hdf5"

# keys for these files should include i-signal instead of n-hadmultmeas
INP1="minosmatch_singlepi0_me1Bmc.hdf5"
INP2="minosmatch_nukecczdefs_127x50x25_xuv_me1Bmc.hdf5"
OUTP="minosmatch_singlepi0_127x50x25_xuv_me1Bmc.hdf5"

python combine_big.py \
  --input1 $INP1 \
  --input2 $INP2 \
  --output $OUTP \
  --match eventids \
  --keys1 i-signal,n-kaons,n-neutrons,n-others,n-pi0s,n-pions,n-protons

python fuelme.py $OUTP 0.83 0.10
