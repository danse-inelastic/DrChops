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
PACKAGE = vectorCompat

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
	AddErrorProp.py\
	AddScalarErrorProp.py  \
	ChannelRange.py\
	CObject.py \
	DivErrorProp.py\
	DivScalarErrorProp.py  \
	DGTS_RebinTof2E_batch.py \
	EBinCalcor.py  \
	ERebinAllInOne.py\
	Fit1DFunction.py\
	He3DetEffic.py \
	MinimizeFunction.py  \
	MonitorNormalizer.py \
	MultErrorProp.py	\
	MultScalarErrorProp.py \
	Normalizer.py  \
	PolynomialFitter.py\
	QBinCalcor.py  \
	QRebinner.py   \
	RDriver.py \
	RebinTof2E.py \
	RebinTof2E_batch.py \
	SimpleFitter.py\
	SimplePeak.py  \
	SubtractErrorProp.py\
	TemplateCObject.py\
	fit_polynomial_QRFactorization.py \
	utils.py   \

export:: export-package-python-modules



# version
# $Id: Make.mm 1431 2007-11-03 20:36:41Z linjiao $

# End of file
