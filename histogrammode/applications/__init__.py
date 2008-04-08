#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \namespace reduction::applications
##
## This package provides reduction applications.
##
## Reduction applications in this package are built from reduciton pyre
## components in package reduction.pyre. 
##
## Currently we only have powder reduction applications.
## The generic powder reduction application is module reduction.applications.PowderReduction.
## Powder reduction applications for LRMECS and PHAROS instruments are in
## reduction.applications.Lrmecs and reduction.applications.Pharos respectively.
##
## \section dir_struct_sec Directory Structure
##
## - applications:  generic reduction applications
##   - applications.gui: gui interfaces for reduction application
##   - Pharos: reduction applications for PHAROS instrument
##    - gui: special gui toolkits for Pharos reduction application
##   - Lrmecs: reduction applications for LRMECS instrument
##    - gui: special gui toolkits for Lrmecs reduction application
##
##

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Aug  7 21:32:19 2006

# End of file 
