#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def page(**kwds):
    from Page import Page
    return Page(**kwds)


def action(*args, **kwds):
    from Action import Action
    return Action( *args, **kwds )


def table(*args, **kwds):
    from Table import Table
    return Table( *args, **kwds )


def column(*args, **kwds):
    from Table import ColumnDescriptor
    return ColumnDescriptor( *args, **kwds )


def slidableGallery(*args, **kwds):
    from SlidableGallery import SlidableGallery
    return SlidableGallery( *args, **kwds )


def plot_2d(*args, **kwds):
    from Plot_2D import Plot_2D
    return Plot_2D(*args, **kwds)


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
