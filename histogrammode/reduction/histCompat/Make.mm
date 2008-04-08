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
PACKAGE = histCompat

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
	__init__.py\
	ARCSDetCalibCalcor.py\
	DGTS_RebinTof2E_batch.py \
	EBinCalcor.py   \
	ERebinAllInOne.py   \
	Fit1DFunction.py   \
	He3DetEffic.py\
	IncidentEnergySolver.py	 \
	LrmecsDetCalibCalcor.py	 \
	MonitorNormalizer.py\
	Normalizer.py   \
	NormCalcor.py   \
	MonitorNormCalcor.py\
	HCNormalizer.py \
	PhiRebinner.py  \
	PolynomialFitter.py \
	QRebinner.py	\
	Rebinner.py	 \
	RebinTof2E.py	 \
	RebinTof2E_batch.py	 \
	SimpleFitter.py \
	VanPlateTx.py   \
	VSampleParams.py\
	functors.py \

export:: export-package-python-modules



# version
# $Id: Make.mm 1484 2008-04-08 15:08:54Z linjiao $

# End of file
