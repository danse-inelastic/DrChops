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

PROJECT = drchops
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS =  
PROJ_CPPTESTS = testItof2IE testItof2IE_batch
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -ldrchops -ljournal


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

testItof2IE: testItof2IE.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testItof2IE.cc $(PROJ_LIBRARIES)

testItof2IE_batch: testItof2IE_batch.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testItof2IE_batch.cc $(PROJ_LIBRARIES)


# version
# $Id: Make.mm 373 2006-01-11 00:26:09Z linjiao $

# End of file
