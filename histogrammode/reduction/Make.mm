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

BUILD_DIRS = \
    core  \
    histCompat  \
    pyre        \
    pyreHC      \
    pyreVC      \
    share   \
    scripting   \
    utils       \
    vectorCompat\

RECURSE_DIRS = $(BUILD_DIRS)

PACKAGE = reduction

#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse



#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py   \
	units.py \
	LoopUtils.py  \



export:: export-python-modules 
	BLD_ACTION="export" $(MM) recurse


include doxygen/default.def
docs: export-doxygen-docs


#the following command should be used to change the urls in
#__init__.py
#sed "s|/<signature>/\(.*\)/html/|<new_signature>/\1/html/index.html|g" __init__.py  > t  && mv t __init__.py

# version
# $Id: Make.mm 1431 2007-11-03 20:36:41Z linjiao $

# End of file
