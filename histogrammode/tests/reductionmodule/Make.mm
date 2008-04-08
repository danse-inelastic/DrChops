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
PROJ_TIDY += *.pyc

PROJ_PYTESTS =  
PROJ_CPPTESTS = testnumpy_support testnumpy_support2
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -lreduction -ljournal -lpython$(PYTHON_VERSION)


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

testnumpy_support: testnumpy_support.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testnumpy_support.cc $(PROJ_LIBRARIES)

testnumpy_support2: testnumpy_support2.cc 
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ testnumpy_support2.cc $(PROJ_LIBRARIES)



# version
# $Id: Make.mm 373 2006-01-11 00:26:09Z linjiao $

# End of file
