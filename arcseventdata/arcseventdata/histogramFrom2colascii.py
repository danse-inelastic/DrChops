#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def convert( filename, name = None,
             xname = 'x', xunit = '1',
             yunit = '1'):
    import read2colascii as r2
    x, y = r2.read( filename )

    if name is None:
        import os
        name = os.path.splitext( os.path.basename( filename ) )[0]
        
    from histogram import histogram
    return histogram( name, [ (xname, x) ], data = y, unit = yunit )


# version
__id__ = "$Id$"

#  End of file 
