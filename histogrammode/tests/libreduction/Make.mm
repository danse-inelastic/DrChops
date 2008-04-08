# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


include local.def

PROJECT = reduction
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS =  
PROJ_CPPTESTS = testHe3DetEffic testVanTxCalcor testRDriver testtof2E testUniversal1DRebinner testReverseIterator testRebinTof2E testRebinTof2E_batch testDGTS_RebinTof2E testDGTS_RebinTof2E_batch testHe3EfficiencyCorrection
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -lreduction -ljournal


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

testHe3DetEffic: testHe3DetEffic.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testHe3DetEffic.cc $(PROJ_LIBRARIES)

testVanTxCalcor:  testVanTxCalcor.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testVanTxCalcor.cc $(PROJ_LIBRARIES)

testRDriver:  testRDriver.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testRDriver.cc $(PROJ_LIBRARIES)

testUniversal1DRebinner: testUniversal1DRebinner.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testUniversal1DRebinner.cc $(PROJ_LIBRARIES)

testReverseIterator: testReverseIterator.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testReverseIterator.cc $(PROJ_LIBRARIES)

testDGTS_RebinTof2E: testDGTS_RebinTof2E.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testDGTS_RebinTof2E.cc $(PROJ_LIBRARIES)

testDGTS_RebinTof2E_batch: testDGTS_RebinTof2E_batch.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testDGTS_RebinTof2E_batch.cc $(PROJ_LIBRARIES)

testRebinTof2E: testRebinTof2E.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testRebinTof2E.cc $(PROJ_LIBRARIES)

testRebinTof2E_batch: testRebinTof2E_batch.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testRebinTof2E_batch.cc $(PROJ_LIBRARIES)

testtof2E: testtof2E.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testtof2E.cc $(PROJ_LIBRARIES)

testHe3EfficiencyCorrection: testHe3EfficiencyCorrection.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testHe3EfficiencyCorrection.cc $(PROJ_LIBRARIES)



# version
# $Id: Make.mm 373 2006-01-11 00:26:09Z linjiao $

# End of file
