#!/bin/bash
DAT=`date +%s`
OUTFILENAME="./merge${DAT}.txt"
JOBNAME="merge${DAT}"
qsub -o $OUTFILENAME job_merge.sh -N $JOBNAME
