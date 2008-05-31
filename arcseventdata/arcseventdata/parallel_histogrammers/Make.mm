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
PACKAGE = parallel_histogrammers


# directory structure

BUILD_DIRS = \
	components \


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
	IdspacingHistogrammer.py \
	IpdpdHistogrammer.py \
	IpdpEHistogrammer.py \
	IpdptHistogrammer.py \
	IqeHistogrammer.py \
	ItofHistogrammer.py \
	ParallelComponent.py \
	ParallelHistogrammer.py \
	__init__.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
