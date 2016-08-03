#!/bin/bash

# keys should include n-hadmultmeas instead of i-signal
# INP1="minosmatch_hadmult_me1Bmc.hdf5"
# INP2="minosmatch_nukecczdefs_127x94x47_me1Bmc.hdf5"
# OUTP="minosmatch_hadmult_127x94x47_xuv_me1Bmc.hdf5"

# keys for these files should include i-signal instead of n-hadmultmeas
INP1="minosmatch_muondat_me1Bmc.hdf5"
INP2="../HDF5files/minosmatch_nukecczdefs_genallz_pcodecap66_127x50x25_xuv_me1Bmc.hdf5"
OUTP="minosmatch_nukecczdefs_genallz_pcodecap66_muondat_127x50x25_xuv_me1Bmc.hdf5"

python combine_big.py \
  --input1 $INP1 \
  --input2 $INP2 \
  --output $OUTP \
  --match eventids \
  --keys1 muon_data

python fuelme.py $OUTP 0.83 0.10
