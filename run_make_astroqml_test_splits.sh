#!/bin/bash

DATADIR="/Users/perdue/Dropbox/Quantum_Computing/hep-qml/data"
FILELIST="
stargalaxy_real
stargalaxy_sim_20190214
strong_lensing_spacebased
"

for file in $FILELIST
do
  python split.py --input "${DATADIR}/${file}.h5" --size 1000
  mv "${DATADIR}/${file}_000.hdf5" "./${file}_cae_test.h5"
  inputlist=`ls ${DATADIR}/${file}_*.hdf5`
  inputlist=($(echo $inputlist | tr " " ","))
  python merge.py --input $inputlist --output "./${file}_cae_train.h5"
done
