#!/bin/bash
#PBS -S /bin/bash
#PBS -N hdf5-prod
#PBS -j oe
#PBS -o ./stmeld_job.txt
# not 2 #PBS -l nodes=gpu2:gpu:ppn=2,walltime=24:00:00
# not 1 #PBS -l nodes=gpu1:gpu:ppn=2,walltime=24:00:00
#PBS -l nodes=1:gpu,walltime=24:00:00
# not short #PBS -l nodes=1:gpu,walltime=6:00:00
#PBS -A minervaG
#PBS -q gpu
#restore to turn off email #PBS -m n

INPATH="/data/perdue/minerva/hdf5/201709"
OUTPATH="/data/perdue/minerva/hdf5/201709"


# print identifying info for this job
echo "Job ${PBS_JOBNAME} submitted from ${PBS_O_HOST} started "`date`" jobid ${PBS_JOBID}"

cat ${PBS_NODEFILE}

cd $HOME
source python_bake_lasagne.sh

cd ${PBS_O_WORKDIR}
echo "PBS_O_WORKDIR is `pwd`"
GIT_VERSION=`git describe --abbrev=12 --dirty --always`
echo "Git repo version is $GIT_VERSION"
DIRTY=`echo $GIT_VERSION | perl -ne 'print if /dirty/'`
if [[ $DIRTY != "" ]]; then
  echo "Git repo contains uncomitted changes! Please commit your changes"
  echo "before submitting a job. If you feel your changes are experimental,"
  echo "just use a feature branch."
  echo ""
  echo "Changed files:"
  git diff --name-only
  echo ""
  # exit 0
fi

filelist='merge_big.py hdf5.py parser.py msg.py check.py merge.py combine_big.py fuelme.py'
for filename in $filelist
do
  cp /home/perdue/hdf5_manipulator/${filename} ${PBS_O_WORKDIR}
done

BASEFILEROOT="minosmatch_kinedat"
BASEFILEROOT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25"
BASEFILEROOT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x94x47"
SAMPLE="me1Bmc"

DOKINE="no"
DOTIME="no"
DOENGY="no"
DO2DET="yes"
DOSPEC="no"

# do kine
if [[ "$DOKINE" == "yes" ]]; then
  INP="${INPATH}/${BASEFILEROOT}_${SAMPLE}_"
  OUT="${OUTPATH}/${BASEFILEROOT}_${SAMPLE}.hdf5"
cat << EOF
python merge_big.py --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
  python merge_big.py --input $INP --output $OUT
  python fuelme.py $OUT 0.86 0.07
fi

# do t
if [[ "$DOTIME" == "yes" ]]; then
  TYPEXT="${BASEFILEROOT}_txtutv"
  INP="${INPATH}/${TYPEXT}_${SAMPLE}_"
  OUT="${OUTPATH}/${TYPEXT}_${SAMPLE}.hdf5"
cat << EOF
python merge_big.py --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
  python merge_big.py --input $INP --output $OUT
  python fuelme.py $OUT 0.86 0.07
fi

# do E
if [[ "$DOENGY" == "yes" ]]; then
  TYPEXT="${BASEFILEROOT}_xuv"
  INP="${INPATH}/${TYPEXT}_${SAMPLE}_"
  OUT="${OUTPATH}/${TYPEXT}_${SAMPLE}.hdf5"
cat << EOF
python merge_big.py --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
  python merge_big.py --input $INP --output $OUT
  python fuelme.py $OUT 0.86 0.07
fi

# do 2d E-t
if [[ "$DO2DET" == "yes" ]]; then
  TYPEXT="${BASEFILEROOT}_xtxutuvtv"
  INP="${INPATH}/${TYPEXT}_${SAMPLE}_"
  OUT="${OUTPATH}/${TYPEXT}_${SAMPLE}.hdf5"
cat << EOF
python merge_big.py --input $INP --output $OUT
python fuelme.py $OUT 0.86 0.07
EOF
  python merge_big.py --input $INP --output $OUT
  python fuelme.py $OUT 0.86 0.07
fi

# do special
if [[ "$DOSPEC" == "yes" ]]; then
  INP="${INPATH}/staging/me1Amc_zzpredpluskine"
  OUT="${OUTPATH}/me1Amc_zzpredpluskine.hdf5"
cat << EOF
python merge_big.py --input $INP --output $OUT
EOF
  python merge_big.py --input $INP --output $OUT
fi


echo "Job ${PBS_JOBNAME} submitted from ${PBS_O_HOST} finished "`date`" jobid ${PBS_JOBID}"
exit 0
