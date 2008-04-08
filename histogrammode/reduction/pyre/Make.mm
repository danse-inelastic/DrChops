# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               T. M. Kelley
#                        (C) 1998-2003 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = reduction
PACKAGE = pyre



BUILD_DIRS = \
  datasource \
  dsm \
  inventory \
  preprocessors \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	Add.py \
	AbstractIdpt2Spe.py \
	Axis.py \
	Composite.py \
	Connectable.py \
	DataStreamModel.py \
	Idpt2Spe.py \
	InplaceSubtract.py \
	Mask.py \
	PhiAxis.py \
	PowderReduction.py \
	Preprocess_All.py \
	Preprocess_MainDataOnly.py \
	Preprocess_Main_and_MT.py \
	Preprocess_Main_and_Calib.py \
	Shapes.py \
	Spe2Sqe.py \
	SpeReducer.py \
	SqeReducer.py \
	Subtract.py \
	__init__.py \
	plotter.py \
	units.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse



# version
# $Id: Make.mm 1431 2007-11-03 20:36:41Z linjiao $

# End of file
