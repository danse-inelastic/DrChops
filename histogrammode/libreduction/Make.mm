# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

include local.def

PROJECT = reduction
PACKAGE = libreduction

PROJ_SAR = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_BINDIR)/$(PACKAGE).$(EXT_SO)
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(PROJ_SAR) $(PROJ_DLL)

PROJ_SRCS = \
	DGTS_RebinTof2E_batch.cc \
	He3DetEffic.cc  \
	He3EfficiencyCorrection.cc  \
	PhiToSlice.cc   \
	QBinCalcor.cc   \
	RDriver.cc \
	RebinTof2E_batch.cc \
	Universal1DRebinner.cc \
	VanPlateAbsorp.cc \
	VecAccum.cc\
	physics.cc \


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# build the library

all: $(PROJ_SAR) export

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ifeq (Win32, ${findstring Win32, $(PLATFORM_ID)})

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_DLL) \
	-Wl,--out-implib=$(PROJ_SAR) $(PROJ_OBJS)

# export
export:: export-headers export-libraries export-binaries

else

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_SAR) $(PROJ_OBJS)


# export
export:: export-headers export-libraries 

endif

EXPORT_HEADERS = \
	DGTS_RebinTof2E.h \
	DGTS_RebinTof2E_batch.h \
	DGTS_RebinTof2E_batch.icc \
	EBinCalcor.h  \
	EBinCalcor.icc\
	ERebinAllInOne.h	\
	ERebinAllInOne.icc  \
	Functor.h  \
	He3DetEffic.h \
	He3DetEffic.icc \
	He3EfficiencyCorrection.h  \
	PhiToSlice.h \
	QBinCalcor.h \
	RebinTof2E.h \
	RebinTof2E_batch.h \
	ReverseIterator.h \
	RDriver.h    \
	Universal1DRebinner.h \
	Universal1DRebinner.icc \
	abs.h \
	exception.h \
	physics.h\
	sort.h \
	tof2E.h \
	utils.h  \
	utils.icc\
	VanPlateAbsorp.h  \
	VecAccum.h

EXPORT_LIBS = $(PROJ_SAR)
EXPORT_BINS = $(PROJ_DLL)



include doxygen/default.def
docs: export-doxygen-docs


# version
# $Id: Make.mm 1444 2007-11-16 16:46:15Z linjiao $

#
# End of file
