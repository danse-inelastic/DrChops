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
PACKAGE = pyre/preprocessors

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractTimeIndependentBackgroundRemover.py \
	AbstractNormalizer.py \
	AbstractIncidentEnergySolver.py \
	ApplyMask.py \
	Calibrator.py \
	Composite.py \
	Connectable.py \
	DataStreamModel.py \
	IdptExtractor.py \
	IncidentEnergySolver_UseElasticPeaks.py \
	IncidentEnergySolver_UseMonitors.py \
	MaskFromUser.py \
	NormalizerUsingIntegratedCurrent.py \
	NormalizerUsingMonitorData.py \
	Step1.py \
	Step1_withTibgWindowPicker.py \
	TimeIndependentBackgroundRemover_AverageOverAllDetectors.py \
	TimeIndependentBackgroundRemover_PerDetector.py \
	TofWindowSelector.py \
	TrivialIncidentEnergySolver.py \
	VDataProcessor.py \
	VPlateDataProcessor.py \
	__init__.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse



# version
# $Id: Make.mm 1000 2006-07-20 06:52:48Z linjiao $

# End of file
