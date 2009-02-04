# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

include local.def

PROJECT = arcseventdata
PACKAGE = libarcseventdata

PROJ_SAR = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_BINDIR)/$(PACKAGE).$(EXT_SO)
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(PROJ_SAR) $(PROJ_DLL)

PROJ_SRCS = \
	Event2d.cc \
	Event2Ei.cc \
	Event2pixd.cc \
	Event2pixEi.cc \
	Event2pixE.cc \
	Event2pixtof.cc \
	Event2QE.cc \
	Event2QQQE.cc \
	Event2tof.cc \
	EventsReader.cc \
	normalize_iqe.cc \
	normalize_iqqqe.cc \
	readPixelPositions.cc \


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
	AbstractMask.h \
	Event.h \
	Event2Quantity.h \
	Event2d.h \
	Event2Ei.h \
	Event2pixd.h \
	Event2pixEi.h \
	Event2pixE.h \
	Event2pixtof.h \
	Event2QE.h \
	Event2QQQE.h \
	Event2tof.h \
	EventsReader.h \
	Exception.h \
	Histogrammer.h \
	Idspacing.h \
	Ipix.h \
	Ipixtof.h \
	Itof.h \
	conversion.h \
	events2histogram.h \
	events2Ix.h \
	events2Ixy.h \
	events2Ixxxx.h \
	events2EvenlySpacedIx.h \
	events2EvenlySpacedIxy.h \
	events2EvenlySpacedIxxxx.h \
	ioutils.h \
	littleEndian2bigEndian.h \
	mappers.h \
	mslice_formating.h \
	mslice_formating.icc \
	normalize_iqe.h normalize_iqe.icc \
	normalize_iqqqe.h normalize_iqqqe.icc \
	pixel_solidangle.h  pixel_solidangle.icc \
	readPixelPositions.h \

EXPORT_LIBS = $(PROJ_SAR)
EXPORT_BINS = $(PROJ_DLL)


# version
# $Id$

#
# End of file
