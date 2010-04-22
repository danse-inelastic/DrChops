#!/usr/bin/env bash

rm -f Ipdpd.h5
ipdpd.py -o Ipdpd.h5 --n 50000 -d 0,4,0.01 -x ARCS.xml -t 20 --journal.info.histogrammer events.dat

python -c "import histogram.hdf as hh; ipdpd = hh.load('Ipdpd.h5', 'I(pdpd)'); Id = ipdpd.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( Id )"

./compareHistogram.py "Ipdpd.h5/I(pdpd)" "oracle/Ipdpd.h5/I(pdpd)"
