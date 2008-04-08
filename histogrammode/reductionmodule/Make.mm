# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               T. M. Kelley
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = reduction
PACKAGE = reductionmodule
MODULE = reduction

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -lreduction -lstdVector -ljournal

PROJ_SRCS = \
	absorptionmod.cc\
	bindings.cc	 \
	exceptions.cc	\
	misc.cc		\
	numpy_support.cc \
	DGTS_RebinTof2E_batch_bdgs.cc \
	EBinCalcor_bdgs.cc  \
	ERebinAllInOne_bdgs.cc \
	He3DetEffic_bdgs.cc \
	RebinTof2E_bdgs.cc \
	RebinTof2E_batch_bdgs.cc \
	QBinCalcor_bdgs.cc \
	RDriver_bdgs.cc	 \
	VecAccum_bdgs.cc \

export:: export-binaries 

include doxygen/default.def
docs: export-doxygen-docs

# version
# $Id: Make.mm 1431 2007-11-03 20:36:41Z linjiao $

# End of file
