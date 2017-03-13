#!/bin/bash

START=0
STOP=0

if [[ $# == 1 ]]; then
  STOP=$1
elif [[ $# > 1 ]]; then
  START=$1
  STOP=$2
fi

SAMPLE=minerva1nofsimc
MUONROOT=minosmatch_muondat_wt

BASEFILEROOT=minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25

# groups in the hdf5 file
# -----------------------
# eventids
# times-u
# times-v
# times-x
TIMELATROOT=${BASEFILEROOT}_txtutv

# groups in the hdf5 file
# -----------------------
# eventids
# hits-u
# hits-v
# hits-x
# planecodes
# segments
# zs
ENGYLATROOT=${BASEFILEROOT}_xuv

# z information + time lattice
DO_Z_TIME="no"

# z information + energy lattice + time lattice
DO_Z_ENGY_TIME="yes"

# z information + energy lattice + time lattice + muon data
DO_Z_ENGY_TIME_MUON="no"

for i in `seq ${START} 1 ${STOP}`
do
  filenum=`echo $i | perl -ne 'printf "%04d",$_;'`

######################################################################
  if [ "$DO_Z_TIME" == "yes" ]; then
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
  fi

######################################################################
  if [ "$DO_Z_ENGY_TIME" == "yes" ]; then

    # merge time lattice and energy lattice hdf5 files into one hdf5 
    # file that contains both time and energy lattices, separately
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

    # merge the time and energy tensors in the combined hdf5 file
    # into combined tensors within that file 
    INP="${ENGYLATROOT}_txtutv_${SAMPLE}_${filenum}.hdf5"
    OUTP="${BASEFILEROOT}_xtxutuvtv_${SAMPLE}_${filenum}.hdf5"
cat << EOF
  time python meld_space_and_time.py --input_file $INP --output_file $OUTP
  time python fuelme.py $OUTP 0.83 0.10
EOF
    time python meld_space_and_time.py --input_file $INP --output_file $OUTP
    time python fuelme.py $OUTP 0.83 0.10

  fi

######################################################################
  if [ "$DO_Z_ENGY_TIME_MUON" == "yes" ]; then
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
  fi

done
