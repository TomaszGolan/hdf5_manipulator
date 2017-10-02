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


START=0
STOP=58

SAMPLE=me1Bmc

INPATH="/data/perdue/minerva/hdf5/201709"
OUTPATH="/data/perdue/minerva/hdf5/201709"

BASEFILEROOT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x50x25"
BASEFILEROOT="minosmatch_nukecczdefs_genallzwitht_pcodecap66_127x94x47"
TIMELATROOT="${BASEFILEROOT}_txtutv"
ENGYLATROOT="${BASEFILEROOT}_xuv"


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

filelist='combine.py meld_space_and_time.py fuelme.py hdf5.py parser.py msg.py check.py extract.py'
for filename in $filelist
do
  cp /home/perdue/hdf5_manipulator/${filename} ${PBS_O_WORKDIR}
done

# do the work...
for i in `seq ${START} 1 ${STOP}`
do
  paddednum=`echo $i | perl -ne 'printf "%04d",$_;'`
  # merge time lattice and energy lattice hdf5 files into one hdf5 
  # file that contains both time and energy lattices, separately
  INP1="${INPATH}/${TIMELATROOT}_${SAMPLE}_${paddednum}.hdf5"
  INP2="${INPATH}/${ENGYLATROOT}_${SAMPLE}_${paddednum}.hdf5"
  OUTP="${OUTPATH}/${ENGYLATROOT}_txtutv_${SAMPLE}_${paddednum}.hdf5"
  FINAL="${OUTPATH}/${BASEFILEROOT}_xtxutuvtv_${SAMPLE}_${paddednum}.hdf5"
cat << EOF
  python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 hits-u,hits-v,hits-x,planecodes,segments,zs \
    --do-not-warn
EOF
  python combine.py \
    --input1 $INP1 \
    --input2 $INP2 \
    --output $OUTP \
    --match eventids \
    --keys2 hits-u,hits-v,hits-x,planecodes,segments,zs \
    --do-not-warn
  # merge the time and energy tensors in the combined hdf5 file
  # into combined tensors within that file 
cat << EOF
  python meld_space_and_time.py --input_file $OUTP --output_file $FINAL
  rm -f $INP1
  rm -f $INP2
  rm -f $OUTP
  python fuelme.py $FINAL 0.86 0.07
EOF
  python meld_space_and_time.py --input_file $OUTP --output_file $FINAL
  rm -f $INP1
  rm -f $INP2
  rm -f $OUTP
  python fuelme.py $FINAL 0.86 0.07
done

# INP1="${INPATH}/${TIMELATROOT}_${SAMPLE}.hdf5"
# INP2="${INPATH}/${ENGYLATROOT}_${SAMPLE}.hdf5"
# OUTP="${OUTPATH}/${ENGYLATROOT}_txtutv_${SAMPLE}.hdf5"
# FINAL="${OUTPATH}/${BASEFILEROOT}_xtxutuvtv_${SAMPLE}.hdf5"
# python meld_space_and_time.py --input_file $OUTP --output_file $FINAL
# rm -f $OUTP
# python fuelme.py $FINAL 0.86 0.07

echo "Job ${PBS_JOBNAME} submitted from ${PBS_O_HOST} finished "`date`" jobid ${PBS_JOBID}"
exit 0
