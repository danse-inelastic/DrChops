# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = reduction
PACKAGE = applications/pyregui_ext/wx

PROJ_TIDY += *.log
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_PYTHON_MODULES = \
	MainFrame.py \
	MainFrameDocBox.py \
	MainWindowApp.py \
	__init__.py \


export:: export-package-python-modules


# version
# $Id: Make.mm 1052 2006-08-02 04:45:45Z linjiao $

# End of file
