#!/usr/bin/env bash

rm -f IpdpE.h5 mslice.spe mslice.phx
events2mslicefiles.py -o IpdpE.h5 --mslice-prefix=mslice --mpirun.nodes=12 --E -50,50,1 -x ARCS.xml -I 98.58  --journal.warning.Event2d=off --journal.info.mpirun  --journal.info.mpi ARCS_297/ARCS_297_neutron_event.dat

diff mslice.spe oracle/mslice_p/mslice.spe
diff mslice.phx oracle/mslice_p/mslice.phx
