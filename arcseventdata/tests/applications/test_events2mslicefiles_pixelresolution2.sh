#!/usr/bin/env bash

rm -f IpdpE.h5 mslice.spe mslice.phx
events2mslicefiles.py -o IpdpE.h5 --mslice-prefix=mslice --n 50000 --E -50,50,1 -x ARCS.xml --pixel-resolution=2 -I 70 -t 20 --journal.warning.Event2d=off --journal.info.mpirun  --journal.info.mpi events.dat

diff mslice.spe oracle/mslice_pr2/mslice.spe
diff mslice.phx oracle/mslice_pr2/mslice.phx
