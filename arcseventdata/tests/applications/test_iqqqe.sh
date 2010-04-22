#!/usr/bin/env bash

rm -f IQQQE.h5
iqqqe.py -o IQQQE.h5 -n 50000 -E=-50,50,10. -Qx=-10,10,1 -Qy=-10,10,1 -Qz=-10,10,1 -x ARCS.xml -I 70 -t 20 --journal.info.iqqqe --journal.info.ParallelHistogrammer --journal.info.histogrammer --journal.info.mpi events.dat

python -c "import histogram.hdf as hh; hist = hh.load('IQQQE.h5', 'I(Qx,Qy,Qz,E)'); summed = hist.sum('Qz').sum('energy'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( summed )"


./compareHistogram.py "IQQQE.h5/I(Qx,Qy,Qz,E)" "oracle/IQQQE.h5/I(Qx,Qy,Qz,E)"