#!/bin/bash

START=0
STOP=0

if [[ $# == 1 ]]; then
  STOP=$1
elif [[ $# > 1 ]]; then
  START=$1
  STOP=$2
fi

SAMPLE=me1Amc

# note
#  python fuelme.py $OUT 0.83 0.10
# was the "historic standard", but switching as of me1Amc energy+time lattice

for i in `seq ${START} 1 ${STOP}`
do
  filenum=`echo $i | perl -ne 'printf "%03d",$_;'`
  INP="../HDF5files/minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_${SAMPLE}_${filenum}.hdf5"
cat << EOF
  python fuelme.py $INP 0.86 0.07
EOF
  time python fuelme.py $INP 0.86 0.07
done
