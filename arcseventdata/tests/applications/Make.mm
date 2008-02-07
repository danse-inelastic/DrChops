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
PROJ_TIDY += *.h5

PROJ_PYTESTS = test_idspacing.sh
PROJ_CPPTESTS = testmpi

PROJ_CPPEXE = 
PROJ_TESTS = $(PROJ_CPPTESTS) $(PROJ_CPPEXE) $(PROJ_PYTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -larcseventdata -ljournal -L$(MPI_LIBDIR)  -lmpich -lrt

PROJ_CXX_FLAGS += -I$(MPI_INCDIR)

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


testmpi: testmpi.cc $(BLD_LIBDIR)/libarcseventdata.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testmpi.cc $(PROJ_LIBRARIES)


# version
# $Id$

# End of file
