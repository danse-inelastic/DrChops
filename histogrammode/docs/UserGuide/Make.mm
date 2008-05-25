# -*- Makefile -*-
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
PACKAGE = UserGuide


PROJ_TIDY += *.log tex-math-equations*

# directory structure

BUILD_DIRS = \
	movies

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


#source files that the main.xml refers to
DOCBOOKSOURCETEMPLATES = \
	Introduction.txml \
	LRMECS.txml \
	PHAROS.txml \
	LRMECS_Reduction_GUI_Tutorial.txml \
	LRMECS_Reduction_Commandline_Tutorial.txml \
	PHAROS_Reduction_GUI_Tutorial.txml \
	PHAROS_Reduction_commandline_Tutorial.txml \
	PHAROS_Parallel_Reduction.txml \
	Prepare_LRMECS_Reduction_Directory.txml \
	Prepare_PHAROS_Reduction_Directory.txml \
	Install.txml \
	InstallFromSource.txml \
	InstallFromSvnRepository.txml \
	InstallFromBinaries.txml \
	GettingStarted.txml \
	Interactive.txml \
	UnixCommands.txml \



include std-docs.def
include docbook/default.def


export-movies: movies
	mkdir -p $(EXPORT_DOCDIR)/movies
	rsync --exclude=.svn -av movies/ $(EXPORT_DOCDIR)/movies


export-materials-for-docs: export-movies


docs:
	$(MM) export-materials-for-docs 
	$(MM) export-docbook-docs


# version
# $Id: Make.mm 444 2006-03-31 07:20:49Z linjiao $

# End of file
