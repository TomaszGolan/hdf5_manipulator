#!/bin/bash
DAT=`date +%s`
OUTFILENAME="./spec${DAT}.txt"
JOBNAME="spec${DAT}"
qsub -o $OUTFILENAME job_spec.sh -N $JOBNAME
