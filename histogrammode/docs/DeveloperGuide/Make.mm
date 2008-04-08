#-*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = reduction
PACKAGE = DeveloperGuide


PROJ_TIDY += *.log tex-math-equations*


# directory structure

BUILD_DIRS = \

OTHER_DIRS = \


RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy:: tidy-tmpxml tidy-tmpxsl
	BLD_ACTION="tidy" $(MM) recurse

export::
	BLD_ACTION="export" $(MM) recurse

test::
	BLD_ACTION="test" $(MM) recurse



#modify the following line to specify the binary of
#xsltproc. maybe this should go into .tools
XSLTPROC = xsltproc


#this is the name of the main xml file of the docbook document
DOCBOOKMAIN = main


DOCBOOKSOURCETEMPLATES = \
	Introduction.txml \
	Architecture.txml \
	PyreComponents.txml \


include docbook/default.def


figures:: uml
	rsync -av uml/ figures/


docs: export-docbook-docs


# version
# $Id: Make.mm 444 2006-03-31 07:20:49Z linjiao $

# End of file
