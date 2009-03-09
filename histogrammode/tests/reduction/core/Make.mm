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

PROJECT = reduction
PACKAGE = tests


RECURSE_DIRS = \
	ARCS \

PROJ_CLEAN += $(PROJ_CPPTESTS)
PROJ_TIDY += *.pyc *.pkl *.xml

PROJ_PYTESTS = runalltestcases.py `#alltests.py 
PROJ_CPPTESTS = 
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) 


#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

tidy::
	BLD_ACTION="tidy" $(MM) recurse

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#


# version
# $Id: Make.mm 469 2006-04-06 23:03:20Z jiao $

# End of file
