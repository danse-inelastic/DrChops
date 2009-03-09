#!/usr/bin/env bash
./clean.sh
ARCSReduceToMsliceFiles.py -I 100 -t 3000,6000,5. -E -90,90,1. -r ARCS_279 -M ARCS_289 -R 0.9 --mpirun.nodes=8 --journal.info.reduction.core.ARCS.ReduceToMslice
