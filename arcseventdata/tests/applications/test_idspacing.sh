#!/usr/bin/env bash

rm -f Id.h5
idspacing.py --o Id.h5 --n 50000 --t 0,4.0,0.01 -x ARCS.xml --journal.warning.Event2d=off --journal.info.mpirun  --journal.info.mpi --journal.info.idspacing events.dat

PlotHist.py Id.h5 "I(d spacing)"
