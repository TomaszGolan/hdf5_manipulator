#!/bin/bash
DAT=`date +%s`
OUTFILENAME="./job_stmeld${DAT}.txt"
JOBNAME="job_stmeld${DAT}"
qsub -o $OUTFILENAME job_spacetime_meld.sh -N $JOBNAME
