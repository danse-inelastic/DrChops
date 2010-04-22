#!/usr/bin/env bash

rm -f Ipdpt.h5
ipdpt.py -o Ipdpt.h5 -n 50000 -t -0,16000,100 -x ARCS.xml events.dat

python -c "import histogram.hdf as hh; ipdpt = hh.load('Ipdpt.h5', 'I(pdpt)'); it = ipdpt.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( it )"

./compareHistogram.py "Ipdpt.h5/I(pdpt)" "oracle/Ipdpt.h5/I(pdpt)"
