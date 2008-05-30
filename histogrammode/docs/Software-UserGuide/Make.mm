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
PACKAGE = Software-UserGuide

# directory structure

PREREQ_DIRS = \
	histogram \
	reduction \
	multiphonon \

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


#source files that the main.xml refers to
DOCBOOKSOURCETEMPLATES = \


include std-docs.def
include docbook/default.def


export-movies: movies
	mkdir -p $(EXPORT_DOCDIR)/movies
	rsync -av movies/ $(EXPORT_DOCDIR)/movies


export-publications: publications
	mkdir -p $(EXPORT_DOCDIR)/publications
	rsync -av publications/ $(EXPORT_DOCDIR)/publications


export-materials-for-docs: export-movies export-publications


docs: 
	$(MM) merge-figures 
	$(MM) merge-movies 
	$(MM) merge-publications 
	$(MM) export-materials-for-docs 
	$(MM) export-docbook-docs


merge-figures::
	mkdir -p figures
	for i in $(PREREQ_DIRS) ; do \
	  rsync -av $$i/figures/ figures/  ; \
	done

merge-movies::
	mkdir -p movies
	for i in $(PREREQ_DIRS) ; do \
	  rsync -av $$i/movies/ movies/  ; \
	done

merge-publications::
	mkdir -p publications
	for i in $(PREREQ_DIRS) ; do \
	  rsync -av $$i/publications/ publications/  ; \
	done


generate-docbook-sources-for-html-output:
	for i in $(PREREQ_DIRS) ; do \
	 cd $$i ; $(MM) generate-docbook-sources-for-html-output ; cd .. ; \
	done
	touch $(DOCBOOKMAINFILE)

generate-docbook-sources-for-latex-output:
	for i in $(PREREQ_DIRS) ; do \
	 cd $$i ; $(MM) generate-docbook-sources-for-latex-output ; cd .. ; \
	done
	touch $(DOCBOOKMAINFILE)



# version
# $Id: Make.mm 444 2006-03-31 07:20:49Z linjiao $

# End of file
