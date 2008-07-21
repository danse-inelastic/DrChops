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
PACKAGE = parallel_histogrammers/components


# directory structure

BUILD_DIRS = \


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
	IqqqeHistogrammer.py \
	ItofHistogrammer.py \
	__init__.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
