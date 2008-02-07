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

PROJECT = arcseventdata
PACKAGE = applications


PROJ_LIBRARIES = -L$(BLD_LIBDIR) -larcseventdata


# directory structure

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse



EXPORT_PYTHON_MODULES = \




l2b: events2Id.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ l2b.cc


PROJ_CPPEXE = \
	l2b \


EXPORT_PYAPPS = \
	events2mslicefiles.py \
	getARCSinstrumentinfo.py \
	getnumberofevents.py \
	idspacing.py \
	ipdpd.py \
	ipdpE.py \
	ipdpt.py \
	iqe.py \
	itof.py \
	createmap-pixelID2position.py \
	mitof.py \
	numpyarray2binary.py \
	pixelpositions2angles.py \


EXPORT_BINS = $(PROJ_CPPEXE) $(EXPORT_PYAPPS)

export-binaries:: $(EXPORT_BINS)

export:: export-binaries release-binaries #export-package-python-modules 


# version
# $Id$

# End of file
