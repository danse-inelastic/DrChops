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
PACKAGE = core

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
	Abstract1DFunctionFitter.py 	\
	AbstractTof2E.py 	\
	AbstractIncidentEnergySolver.py \
	AbstractTimeIndependentBackgroundRemover.py \
	AbstractIdpt2Spe.py	\
	AbstractIdpt2Sqe.py	\
	ApplyMaskToHistogram.py \
	DifferentialEvolution1DFunctionFitter.py \
	HistogramCombiner.py \
	IdptExtractor.py	\
	Idpt2Spe_a.py		\
	Idpt2Sqe.py		\
	IncidentEnergySolver_UseMonitors.py \
	IncidentEnergySolver_UseElasticPeaks.py \
	LoopUtils.py \
	MaskFromVanadiumData.py \
	TimeIndependentBackgroundRemover.py \
	TimeIndependentBackgroundRemover_AverageOverAllDetectors.py \
	ParallelComponent.py		\
	Spe2Sqe.py		\
	Tof2E.py 		\
	VDataProcessor.py	\
	VanadiumTransmissionCalculator.py\
	getDetectorInfo.py 	\
	getPixelInfo.py 	\
	mask.py          	\
	numeric_functors.py 	\
	utils.py 		\
	__init__.py		\


export:: export-package-python-modules



# version
# $Id: Make.mm 1212 2006-11-21 21:59:44Z linjiao $

# End of file
