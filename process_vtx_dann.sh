#!/bin/bash

REMDIR=/phihome/perdue/caffe/data/minerva/vertex

# INPBASE=minosmatch_nukecczdefs_genallz_pcodecap66_127x50x25_xuv_me1Bmc
# INPNAME=${INPBASE}.hdf5
# python split_big.py --input $REMDIR/$INPNAME --size 50000
# NMAX=`ls $REMDIR/${INPBASE}_*.hdf5 | wc -l`
# NMAX=$((NMAX - 1))

# for i in `seq 0 1 $NMAX`
# do
#   filenum=`echo $i | perl -ne 'printf "%03d",$_;'`
#   echo $filenum
#   cp $REMDIR/${INPBASE}_${filenum}.hdf5 $REMDIR/unrenamed/${INPBASE}_${filenum}.hdf5
#   python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
#     --dataset hits-x --name hits-x-MEMC
#   python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
#     --dataset hits-u --name hits-u-MEMC
#   python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
#     --dataset hits-v --name hits-v-MEMC
# done

INPBASE=minosmatch_nukecczdefs_genallz_pcodecap66_127x50x25_xuv_minerva1mc
INPNAME=${INPBASE}.hdf5
python split_big.py --input $REMDIR/$INPNAME --size 50000
NMAX=`ls $REMDIR/${INPBASE}_*.hdf5 | wc -l`
NMAX=$((NMAX - 1))

for i in `seq 0 1 $NMAX`
do
  filenum=`echo $i | perl -ne 'printf "%03d",$_;'`
  echo $filenum
  cp $REMDIR/${INPBASE}_${filenum}.hdf5 $REMDIR/unrenamed/${INPBASE}_${filenum}.hdf5
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-x --name hits-x-LEMC
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-u --name hits-u-LEMC
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-v --name hits-v-LEMC
done

INPBASE=minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25_xuv_minerva13Bmc
INPNAME=${INPBASE}.hdf5
python split_big.py --input $REMDIR/$INPNAME --size 50000
NMAX=`ls $REMDIR/${INPBASE}_*.hdf5 | wc -l`
NMAX=$((NMAX - 1))

for i in `seq 0 1 $NMAX`
do
  filenum=`echo $i | perl -ne 'printf "%03d",$_;'`
  echo $filenum
  cp $REMDIR/${INPBASE}_${filenum}.hdf5 $REMDIR/unrenamed/${INPBASE}_${filenum}.hdf5
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-x --name hits-x-LEMC
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-u --name hits-u-LEMC
  python rename_dataset.py --input $REMDIR/${INPBASE}_${filenum}.hdf5 \
    --dataset hits-v --name hits-v-LEMC
done
