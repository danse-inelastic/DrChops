#!/usr/bin/env bash

rm -f IQE.h5
iqe.py -o IQE.h5 --n 50000 -E -50,50,1. -Q 0,13,0.1 -x ARCS.xml -I 70 -t 20 --journal.info.iqe events.dat

PlotHist.py IQE.h5 "I(Q,E)"

