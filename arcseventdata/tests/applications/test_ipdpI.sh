#!/usr/bin/env bash

rm -f IpdpI.h5
ipdpI.py -o IpdpI.h5 --n 50000 -I 0,100,1. -x ARCS.xml -t 20 --journal.info.histogrammer events.dat

python -c "import histogram.hdf as hh; ipdpI = hh.load('IpdpI.h5', 'I(pdpI)'); II = ipdpI.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( II )"

