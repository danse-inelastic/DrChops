#!/usr/bin/env bash

rm -f Id.h5
#mpirun -n 5  mpipython.exe `which idspacing.py` -o Id.h5 -n 50000 -t0,4.0,0.01 -x ARCS.xml events.dat
idspacing.py -o Id.h5 -n 50000 -t 0,4.0,0.01 -x ARCS.xml --mpirun.nodes=4 --journal.warning.Event2d=off --journal.info.mpirun  --journal.info.mpi --journal.info.idspacing  events.dat
#idspacing.py -o Id.h5 -n 50000 -t 0,4.0,0.01 -x ARCS.xml --mpirun.nodes=4 --journal.info.mpirun --journal.debug.mpirun --journal.info.mpi events.dat

PlotHist.py Id.h5 "I(d spacing)"

./compareHistogram.py "Id.h5/I(d spacing)" "oracle/Id.h5/I(d spacing)"
