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

# directory structure

#--------------------------------------------------------------------------
all: export
#

CP_RF = cp -rf
EXPORT_DATADIRS = \
    Lrmecs \
    Pharos \
    icons \


EXPORT_SHAREDIR=$(EXPORT_ROOT)/share
SHARE_DEST =  $(EXPORT_SHAREDIR)/$(PROJECT)/resources

export:: export-package-data

export-package-data:: $(EXPORT_DATADIRS)
	mkdir -p $(SHARE_DEST); \
	for x in $(EXPORT_DATADIRS); do { \
            if [ -d $$x ]; then { \
	        $(CP_RF) $$x $(SHARE_DEST); \
            } fi; \
        } done


# version
# $Id: Make.mm 788 2006-02-22 05:33:34Z linjiao $

# End of file
