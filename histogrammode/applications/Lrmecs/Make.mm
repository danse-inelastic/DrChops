# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = reduction
PACKAGE = applications/Lrmecs

PROJ_TIDY += *.log
PROJ_CLEAN =

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

#--------------------------------------------------------------------------
#


EXPORT_PYTHON_MODULES = \
	__init__.py \
	Outputs.py \


EXPORT_BINS = \
	lrmecs2ascii \

export:: export-binaries release-binaries export-package-python-modules

cleanbins:
	for i in $(EXPORT_BINS) ; do \
	  rm -f $EXPORT_ROOT/bin/$$i ; \
	done

# version
# $Id: Make.mm 913 2006-05-09 08:43:23Z jiao $

# End of file
