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
PACKAGE = interactive

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
	FacilityFrontEnd.py	\
	Fit1DFunction.py	\
	Fit1DGaussian.py	\
	FunctorFromFunction.py	\
	GetCalibrationConstants.py	\
	GetExperimentalRun.py	\
	HistogramPlotter.py	\
	Idpt2Spe.py	\
	Idpt2Sqe.py	\
	IncidentEnergySolver.py \
	NormalizationConstantCalculator.py \
	Spe2Sqe.py \
	TimeIndependentBackgroundRemover.py \
	_utils.py		\
	__init__.py		\


export:: export-package-python-modules



# version
# $Id: Make.mm 1212 2006-11-21 21:59:44Z linjiao $

# End of file
