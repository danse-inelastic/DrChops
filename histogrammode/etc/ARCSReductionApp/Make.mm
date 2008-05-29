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

PROJECT = ARCSReductionApp
PACKAGE = 

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
# export

EXPORT_ETC = \
	ARCSMeasurement.odb \
	ARCSReductionApp.pml \
	IncidentEnergySolver_UseElasticPeaks.odb \
	IncidentEnergySolver_UseElasticPeaks.pml \
	NormalizerUsingIntegratedCurrent.odb \
	Preprocess_All.odb \
	Preprocess_All.pml \
	Preprocess_Main_and_Calib.odb \
	Preprocess_Main_and_Calib.pml \
	Preprocess_Main_and_MT.odb \
	Preprocess_Main_and_MT.pml \
	Preprocess_MainDataOnly.odb \
	Preprocess_MainDataOnly.pml \
	TimeIndependentBackgroundRemover_AverageOverAllDetectors.odb \
	TimeIndependentBackgroundRemover_PerDetector.odb \
	VPlateDataProcessor.odb \
	preStep1.odb \
	preStep1.pml \
	preStep1_withTibgWindowPicker.odb \
	__vault__.odb \


export:: export-etc

# version
# $Id: Make.mm 818 2006-03-01 06:06:22Z linjiao $

# End of file
