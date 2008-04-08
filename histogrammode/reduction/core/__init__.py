#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core
## This package contains all core reduction operators.
## This package should not be used by end-users directly.
## End-user should use package reduction.scripting
## or the reduction applications.
##
## An operator that could have multiple implementaions is
## implemented with one abstract class and several implementation
## classes.
##
## Any abstract base class starts with 'Abstract...'.
##
## Operators here are exposed to users in reduction.scripting
## package through FacilityFrontEnd. And they are also
## wrapped into pyre components and the reduction.pyre package.
##


# version
__id__ = "$Id$"

# End of file 
