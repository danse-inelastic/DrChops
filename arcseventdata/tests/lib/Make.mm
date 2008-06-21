# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = arcseventdata
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS = 
PROJ_CPPTESTS = test_Histogrammer1 test_Histogrammer2 test_Histogrammer4 \
	test_Event2Quantity \
	test_events2Ix test_EventsReader test_Event2d \
	test_events2EvenlySpacedIx \
	test_events2EvenlySpacedIxy \
	test_events2EvenlySpacedIxxxx \
	test_mslice_formating \
	test_Event2tof \
	test_Event2QE \
	test_Event2QQQE \
	test_Event2pixd \
	test_normalize_iqe \

PROJ_CPPEXE = 
PROJ_TESTS = $(PROJ_CPPTESTS) $(PROJ_CPPEXE) $(PROJ_PYTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -larcseventdata -ljournal


#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

test_Histogrammer1: test_Histogrammer1.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Histogrammer1.cc $(PROJ_LIBRARIES)

test_Histogrammer2: test_Histogrammer2.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Histogrammer2.cc $(PROJ_LIBRARIES)

test_Histogrammer4: test_Histogrammer4.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Histogrammer4.cc $(PROJ_LIBRARIES)

test_Event2Quantity: test_Event2Quantity.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2Quantity.cc $(PROJ_LIBRARIES)

test_EventsReader: test_EventsReader.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_EventsReader.cc $(PROJ_LIBRARIES)

test_events2Ix: test_events2Ix.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_events2Ix.cc $(PROJ_LIBRARIES)

test_Event2d: test_Event2d.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2d.cc $(PROJ_LIBRARIES)

test_Event2pixd: test_Event2pixd.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2pixd.cc $(PROJ_LIBRARIES)

test_Event2tof: test_Event2tof.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2tof.cc $(PROJ_LIBRARIES)

test_Event2QE: test_Event2QE.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2QE.cc $(PROJ_LIBRARIES)

test_Event2QQQE: test_Event2QQQE.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_Event2QQQE.cc $(PROJ_LIBRARIES)

test_events2EvenlySpacedIx: test_events2EvenlySpacedIx.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_events2EvenlySpacedIx.cc $(PROJ_LIBRARIES)

test_events2EvenlySpacedIxy: test_events2EvenlySpacedIxy.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_events2EvenlySpacedIxy.cc $(PROJ_LIBRARIES)

test_events2EvenlySpacedIxxxx: test_events2EvenlySpacedIxxxx.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_events2EvenlySpacedIxxxx.cc $(PROJ_LIBRARIES)

test_mslice_formating: test_mslice_formating.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_mslice_formating.cc $(PROJ_LIBRARIES)

test_normalize_iqe: test_normalize_iqe.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_normalize_iqe.cc $(PROJ_LIBRARIES)



# version
# $Id$

# End of file
