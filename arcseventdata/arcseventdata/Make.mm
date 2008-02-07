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
PACKAGE = arcseventdata


# directory structure

BUILD_DIRS = \
	pyre_support \


OTHER_DIRS = \


RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	createmap_pixelID2position.py \
	events2Ipdp.py \
	events2Ipdpd.py \
	events2IpdpE.py \
	events2IQE.py \
	events2Ipdpt.py \
	events2Itof.py \
	events2Idspacing.py \
	getinstrumentinfo.py \
	getpixelinfo.py \
	histogramFrom2colascii.py \
	longpixelID.py \
	monitorData.py \
	mslice_spe_writer.py \
	pixelpositions2angles.py \
	read2colascii.py \
	units.py \
	__init__.py \
	GetDetectorAxesInfo.py \
	ParallelComponent.py \
	ParallelHistogrammer.py \


export:: export-python-modules

# version
# $Id$

# End of file
