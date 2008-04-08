#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat
## Vector- and list-level classes for reduction package
##
## This layer is the joint point between c++ and python.
##
## All c++ codes are implemented to deal with "vector"-like objects, e.g., energy bins.
## The vectorCompat python package accepts vector arguments and call the corresponding
## c++ methods to do the real work
##
## There are several categories of tools in this subpackage.
##
##  - classes that connects to c++ reduction utilities
##   - drivers to do rebinning
##    - ERebinAllInOne.py
##    - QRebinner.py
##    - RDriver.py
##   - bin calculators
##    - EBinCalcor.py
##    - QBinCalcor.py
##   - other calculators
##    - He3DetEffic.py
##  - fundamental classes that are used to connect python object and c object
##    - TemplateCObject.py
##    - CObject.py 
##  - fitting utilities
##    - fit_polynomial_QRFactorization.py
##    - PolynomialFitter.py
##    - SimpleFitter.py
##  - error propagators (obsolete):
##    - AddErrorProp.py
##    - AddScalarErrorProp.py
##    - DivErrorProp.py
##    - DivScalarErrorProp.py
##    - MultErrorProp.py
##    - MultScalarErrorProp.py
##    - SubtractErrorProp.py
##
## Modules for rebinning deserve a few more words here:
## 
## The goal of reduction is to convert raw data into sth like S(phi,E) or S(Q,E).
## Currently this is done by binning and rebinning.
## To do (re)binning, we need two categories of utilities:
##     - bin calculators
##     - rebin drivers
##
## For bin calculators, we have
##   \arg EBinCalcor calculate energy bins out of tof bins
##   \arg QBinCalcor calculate momentum bins out of phi bins
##
## For rebinning drivers, we have
##   \arg ERebinAllInOne rebin data in tof bins to given energy bins
##   \arg QRebinner rebin data in phi bins to given Q bins
##   \arg RDriver rebin data of I(det, pix, E) to I(phi,E)
  
 


def add( vect1, vect2, output):
    " output = vect1+vect2"
    from stdVector import add
    return add(vect1, vect2, output)


def divide( vect1, vect2, output):
    " output = vect1/vect2"
    from stdVector import divide
    return divide(vect1, vect2, output)


def multiply( vect1, vect2, output):
    " output = vect1*vect2"
    from stdVector import multiply
    return multiply(vect1, vect2, output)


def subtract( vect1, vect2, output):
    " output = vect1-vect2"
    from stdVector import subtract
    return subtract(vect1, vect2, output)


# version
__id__ = "$Id: __init__.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
