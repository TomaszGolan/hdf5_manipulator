#!/bin/bash

for i in {0..80}
do
  filenum=`echo $i | perl -ne 'printf "%04d",$_;'`
  # ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_vtxinfo_me1Bmc_${filenum}.hdf5 | grep "No"
  # ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_txtutv_me1Bmc_${filenum}.hdf5 | grep "No"
  # ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_minerva13Cmc_${filenum}.hdf5 | grep "No"
  ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_minerva1nofsimc_${filenum}.hdf5 | grep "No"
  ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_txtutv_minerva1nofsimc_${filenum}.hdf5 | grep "No"
  ls minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xtxutuvtv_minerva1nofsimc_${filenum}.hdf5 | grep "No"
done
