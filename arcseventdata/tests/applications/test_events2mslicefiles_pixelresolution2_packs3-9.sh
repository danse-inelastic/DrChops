#!/usr/bin/env bash

rm -f IpdpE.h5 mslice.spe mslice.phx
events2mslicefiles.py -o IpdpE.h5 --mslice-prefix=mslice --n 50000 --E -50,50,1 -x ARCS.xml -packs=3,9 --pixel-resolution=2 -I 70 -t 20 --journal.warning.Event2d=off --journal.info.mpirun  --journal.info.mpi events.dat
