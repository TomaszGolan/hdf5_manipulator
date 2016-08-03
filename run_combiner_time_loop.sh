#!/bin/bash

START=0
STOP=0

if [[ $# == 1 ]]; then
  STOP=$1
elif [[ $# > 1 ]]; then
  START=$1
  STOP=$2
fi

SAMPLE=me1Bmc
MUONROOT=minosmatch_muondat_wt

# groups in the hdf5 file
# -----------------------
# eventids
# times-u
# times-v
# times-x
TIMELATROOT=minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv

# groups in the hdf5 file
# -----------------------
# eventids
# hits-u
# hits-v
# hits-x
# planecodes
# segments
# zs
ENGYLATROOT=minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv



for i in `seq ${START} 1 ${STOP}`
do
  filenum=`echo $i | perl -ne 'printf "%04d",$_;'`

  # # z information + time lattice
  INP1="${TIMELATROOT}_${SAMPLE}_${filenum}.hdf5"
  INP2="${ENGYLATROOT}_${SAMPLE}_${filenum}.hdf5"
  OUTP="${TIMELATROOT}_vtxinfo_${SAMPLE}_${filenum}.hdf5"

cat << EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 planecodes,segments,zs \
    --do-not-warn --show-progress

  python fuelme.py $OUTP 0.83 0.10
EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 planecodes,segments,zs \
    --do-not-warn --show-progress

  time python fuelme.py $OUTP 0.83 0.10


  # z information + energy lattice + time lattice
  INP1="${TIMELATROOT}_${SAMPLE}_${filenum}.hdf5"
  INP2="${ENGYLATROOT}_${SAMPLE}_${filenum}.hdf5"
  OUTP="${ENGYLATROOT}_txtutv_${SAMPLE}_${filenum}.hdf5"

cat << EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 hits-u,hits-v,hits-x,planecodes,segments,zs \
    --do-not-warn --show-progress
EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 hits-u,hits-v,hits-x,planecodes,segments,zs \
    --do-not-warn --show-progress

  time python fuelme.py $OUTP 0.83 0.10


  # z information + energy lattice + time lattice + muon data
  INP1="${ENGYLATROOT}_txtutv_${SAMPLE}_${filenum}.hdf5"
  INP2="minosmatch_muondat_wt_${SAMPLE}_${filenum}.hdf5"
  OUTP="${ENGYLATROOT}_txtutv_muondat_${SAMPLE}_${filenum}.hdf5"

cat << EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 muon_data \
    --do-not-warn --show-progress
EOF
  time python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 muon_data \
    --do-not-warn --show-progress

  time python fuelme.py $OUTP 0.83 0.10

done
