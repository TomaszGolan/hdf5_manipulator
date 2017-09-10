#!/bin/bash
DAT=`date +%s`
OUTFILENAME="./stmeld${DAT}.txt"
JOBNAME="stmeld${DAT}"
qsub -o $OUTFILENAME job_spacetime_meld.sh -N $JOBNAME
