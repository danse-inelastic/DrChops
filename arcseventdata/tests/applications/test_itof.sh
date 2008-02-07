#!/usr/bin/env bash

rm -f Itof.h5
itof.py -o Itof.h5 -n 50000 -t -0,16000,100 -x ARCS.xml events.dat

PlotHist.py Itof.h5 "I(tof)"

