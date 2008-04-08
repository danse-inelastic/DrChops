# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = PharosReductionApp
PACKAGE = 

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
# export

EXPORT_ETC = \
	IncidentEnergySolver_UseElasticPeaks.odb \
	NormalizerUsingIntegratedCurrent.odb \
	PharosMeasurement.odb \
	PharosReductionApp.pml \
	Preprocess_All.pml \
	Preprocess_All.odb \
	Preprocess_MainDataOnly.pml \
	Preprocess_MainDataOnly.odb \
	Preprocess_Main_and_MT.pml \
	Preprocess_Main_and_MT.odb \
	Preprocess_Main_and_Calib.pml \
	Preprocess_Main_and_Calib.odb \
	VPlateDataProcessor.odb \
	preStep1.odb \
	preStep1.pml \
	preStep1_withTibgWindowPicker.odb \
	preStep1_withTibgWindowPicker.pml \
	__vault__.odb
#	preStep1_main.odb \
#	preStep1_main.pml \
#	preStep1_mt.odb \
#	preStep1_mt.pml \
#	__vault__.odb


export:: export-etc

# version
# $Id: Make.mm 818 2006-03-01 06:06:22Z linjiao $

# End of file
