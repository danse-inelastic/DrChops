#!/usr/bin/env bash

rm -f m1Itof.h5
mitof.py -o m1Itof.h5 ARCS_120_bmon1_histo.dat

PlotHist.py m1Itof.h5 "I(tof)"

