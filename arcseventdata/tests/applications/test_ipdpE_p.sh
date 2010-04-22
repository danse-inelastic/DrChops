#!/usr/bin/env bash

rm -f IpdpE.h5
ipdpE.py -o IpdpE.h5 -n 50000 -E -50,50,1 -x ARCS.xml -I 70 -t 20 --mpirun.nodes=2  --journal.info.mpi --journal.info.ipdpE --journal.info.histogrammer events.dat
#ipdpE.py -o IpdpE.h5 -n 50000 -E -50,50,1 -x ARCS.xml -I 70 -t 20 --mpirun.nodes=2  --journal.info.mpi --journal.warning.arcseventdata.Histogrammer2=off --journal.info.ipdpE events.dat


python -c "import histogram.hdf as hh; ipdpE = hh.load('IpdpE.h5', 'I(pdpE)'); IE = ipdpE.sum('detectorpackID').sum('detectorID').sum('pixelID'); from histogram.plotter import defaultPlotter as plotter; plotter.plot( IE )"

./compareHistogram.py "IpdpE.h5/I(pdpE)" "oracle/IpdpE.h5/I(pdpE)"
