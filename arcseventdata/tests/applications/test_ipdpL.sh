#!/usr/bin/env bash

rm -f IpdpL.h5
ipdpL.py -o IpdpL.h5 --n 50000 -L 0,10,0.1 -x ARCS.xml -t 20 --journal.info.histogrammer events.dat

python -c "import histogram.hdf as hh; ipdpL = hh.load('IpdpL.h5', 'I(pdpL)'); IL = ipdpL.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( IL )"

./compareHistogram.py "IpdpL.h5/I(pdpL)" "oracle/IpdpL.h5/I(pdpL)"
