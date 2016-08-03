#!/bin/bash

START=0
STOP=0

if [[ $# == 1 ]]; then
  STOP=$1
elif [[ $# > 1 ]]; then
  START=$1
  STOP=$2
fi

SAMPLE=minerva1mc

for i in `seq ${START} 1 ${STOP}`
do
  filenum=`echo $i | perl -ne 'printf "%04d",$_;'`

  INP1="minosmatch_nukecczdefs_tracker_127x72x36_${SAMPLE}_${filenum}.hdf5"
  INP2="minosmatch_hadmult_${SAMPLE}_${filenum}.hdf5"
  OUTP="minosmatch_hadmult_tracker_127x72x36_${SAMPLE}_${filenum}.hdf5"

cat << EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 n-hadmultmeas,n-kaons,n-neutrons,n-others,n-pi0s,n-pions,n-protons \
    --do-not-warn --show-progress

  python fuelme.py $OUTP 0.83 0.10
EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 n-hadmultmeas,n-kaons,n-neutrons,n-others,n-pi0s,n-pions,n-protons \
    --do-not-warn --show-progress

  python fuelme.py $OUTP 0.83 0.10

  INP1="minosmatch_nukecczdefs_tracker_127x72x36_${SAMPLE}_${filenum}.hdf5"
  INP2="minosmatch_singlepi0_${SAMPLE}_${filenum}.hdf5"
  OUTP="minosmatch_singlepi0_tracker_127x72x36_${SAMPLE}_${filenum}.hdf5"

cat << EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 i-signal,n-hadmultmeas,n-kaons,n-neutrons,n-others,n-pi0s,n-pions,n-protons \
    --do-not-warn --show-progress

  python fuelme.py $OUTP 0.83 0.10
EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 i-signal,n-hadmultmeas,n-kaons,n-neutrons,n-others,n-pi0s,n-pions,n-protons \
    --do-not-warn --show-progress

  python fuelme.py $OUTP 0.83 0.10

done
