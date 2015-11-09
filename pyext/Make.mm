# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = drchops
PACKAGE = drchopsmodule
MODULE = drchops

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -ldrchops -ljournal

PROJ_SRCS = \
	IpixE2IphiE_bdgs.cc \
	Itof2IE_batch_bdgs.cc \
	Zt2Zxy_bdgs.cc \
	bindings.cc \
	exceptions.cc \
	misc.cc \
	numpy_support.cc \


# version
# $Id$

# End of file
