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

PROJECT = arcseventdata
PACKAGE = arcseventdatamodule
MODULE = arcseventdata

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -larcseventdata -ljournal

PROJ_SRCS = \
	bindings.cc \
	exceptions.cc \
	misc.cc \
	numpy_support.cc \
	wrap_events2EvenlySpacedIx.cc \
	wrap_events2EvenlySpacedIxy.cc \
	wrap_events2EvenlySpacedIxxxx.cc \
	wrap_mslice_formating.cc \
	wrap_normalize_iqe.cc \
	wrap_normalize_iqqqe.cc \
	wrap_readevents.cc \
	wrap_readpixelpositions.cc \


# version
# $Id$

# End of file
