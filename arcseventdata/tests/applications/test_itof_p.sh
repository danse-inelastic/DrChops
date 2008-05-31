#!/usr/bin/env bash

rm -f Itof.h5
itof.py -o Itof.h5 -n 50000 -t -0,16000,100 -x ARCS.xml  --mpirun.nodes=4  --journal.info.mpirun  --journal.info.mpi --journal.info.idspacing  --journal.info.histogrammer   events.dat

PlotHist.py Itof.h5 "I(tof)"

