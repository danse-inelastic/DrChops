#!/usr/bin/env bash

out=IhklE-compressed.h5
rm -f $out
ihkle.py -o $out --n 50000 -E -50,50,10. --hh=-10,10,1 --kk=-10,10,1 --ll=-10,10,1 -x ARCS.xml -I 70 -t 20 --compression=9 --journal.info.ihkle --journal.info.ParallelHistogrammer --journal.info.histogrammer --journal.info.mpi events.dat

python -c "import histogram.hdf as hh; hist = hh.load('$out', 'I(h,k,l,E)'); summed = hist.sum('l').sum('energy'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( summed )"


