#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.pyre
## pyre components for reduction package
##
##
## Basic reduction steps:
##    - determine incident energy
##    - determine normalization
##    - determine calibrations
##    - reduce main data (sample data) to s(phi,E)
##    - convert to s(Q,E)
##
## Followiing are major pyre components:
##
##
## EiSolver
##
##   interface:
##      -  solve(...)  --> return the incident energy
##
##   implementation:
##      - a base class that fixes the interface: EiSolver
##      - several solid implementations
##         - simple ei solver (get ei from user input): SimpleEiSolver
##         - calculate ei from monitor data: EiSolverUsingMonitorData
##
##
##
## Normalizer
##
##   interface:
##      -  __call__( ... ) --> normalize input histogram (collection)
##
##   implementation:
##      - a base class that fixes the interface: Normalizer.Normalizer
##      - several solid implementations
##         - simple normalizer that does no normalization: Normalizer.NullNormalizer
##         - normalize by using monitor data: NormalizerUsingMonitorData.NormalizerUsingMonitorData
##         - normalize by using integrated modeartor current: NormalizerUsingIntegratedCurrent.NormalizerUsingIC
##
##
## VCalibration
##
##   interface:
##     -  calcCalibrations( .. ) --> calculate calibration constants given incident energy, the vanadium dataset
##
##   implementation:
##      - a base class that fixes the interface: VCalibration.VCalibration
##      - several solid implementations
##         - simple one that do no calibration: VCalibration.NoCalibration
##         - do calibration detector by detector: VCalib_Det.VCalibration
##
##
## DetEfficiency.DetEffCalcor
##
##   interface:
##     -   calcEffHist( energyAxis, ei) --> calculate detector efficiencey given an energy axis. The energy is the final energy of neutrons.
##
##   implementation:
##     -  a base class that fixes the interface: DetEfficiency.DetEffCalcor
##     -  several solid implementations
##         - a simple implementation: SimpleDetEfficiency.SimpleDetEfficiency
##
##
## SpeReducer
##
##   interface:
##      -  reduce( ei, histCollection, instrument, geometer) --> reduce histCollection to S(phi, E) given calibration constants, incident energy, and measurement
##
##   implementation:
##      - a base class that fixes the interface: SpeReducer
##      - one solid implementation: SimpleSpeReducer
##
##
##
## Spe2Sqe
##
##   interface:
##     -   __call__( ei, spe ) --> transform S(phi, E) to S(Q,E)
##
##
##   implementation:
##     -   one solid implementation




# version
__id__ = "$Id: __init__.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
