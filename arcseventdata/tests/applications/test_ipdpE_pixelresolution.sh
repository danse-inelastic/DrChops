#!/usr/bin/env bash

rm -f IpdpE.h5
ipdpE.py -o IpdpE.h5 --pixel-resolution=2 --n 50000 -E -50,50,1 -x ARCS.xml -I 70 -t 20 --journal.info.histogrammer events.dat

python -c "import histogram.hdf as hh; ipdpE = hh.load('IpdpE.h5', 'I(pdpE)'); IE = ipdpE.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( IE )"

