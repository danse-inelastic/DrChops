# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = reduction
PACKAGE = applications

# directory structure

BUILD_DIRS = \
    gui \
    pyregui_ext \
    Lrmecs \
    Pharos \
    ARCSSimu \

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
	NewRun_PyreApp.py \
        __init__.py \


EXPORT_BINS = \
	ARCSReductionApp.py \
	ARCSReduceVanadiumData.py \
	LrmecsReductionApp.py \
	MCSimReductionApp.py \
	PharosReductionApp.py \
	PharosReductionApp_Parallel.py \
	PlotSpe.py \
	PlotSqe.py \
	PowderReductionApp.py \
	PowderReductionApp_Parallel.py \
	makePixelInfoCache.py \
	plotcalibrationresults.py \
	plotiphi.py \
	plotitof.py \
	plotmonitoritof.py \
	toMslice.py \
	wxARCSReductionApp.py \
	wxLrmecsReductionApp.py \
	wxPharosReductionApp.py \


include doxygen/default.def


export:: $(EXPORT_BINS) make-executables export-binaries release-binaries export-package-python-modules #export-docs


make-executables:
	for i in $(EXPORT_BINS) ; do \
	  chmod +x $$i ;\
	done


WEBSERVER=http://131.215.30.242:5001

%.py: %.py.t
	cat $< | sed 's|xxxDoxygenDocsxxx|$(DOXYGEN_DOCS)|g' | sed 's|xxxWEBSERVERxxx|$(WEBSERVER)|g'  >   $@


APPS_GENERATED_FROM_TEMPALATES = \
	ARCSReductionApp.py \
	LrmecsReductionApp.py \
	PharosReductionApp.py \
	MCSimReductionApp.py \

PROJ_CLEAN += $(APPS_GENERATED_FROM_TEMPALATES)

# version
# $Id: Make.mm 1440 2007-11-12 22:59:42Z linjiao $

# End of file
