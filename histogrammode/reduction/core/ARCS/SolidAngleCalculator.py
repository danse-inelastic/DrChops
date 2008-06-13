#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction import units
meter = units.length.meter
cm = units.length.cm


class SolidAngleCalculator:

    '''calculate solid angles of pixels for ARCS instrument

    For ARCS, all tubes are vertical. The solid angle is

      pixelarea * cos(theta) / r**2

    where r is the distance from sample to pixel, pixelarea is the area
    of a pixel (2*radius*height), and theta is the angle between kf and
    the horizontal plane.
    '''

    def __call__(self, solidangles, pixelpositions, pixelradius = 1.27*cm, pixelheight = 1.*meter/128):
        '''
        solidangles: the solid angle array to hold result
        pixelpositions: the pixel positions
        pixelradius: pixel radius (with unit)
        pixelheight: pixel height (with unit)
        '''

        #save shapes
        ppshape = pixelpositions.shape
        pixelpositions.shape = -1, 3
        sashape = solidangles.shape
        solidangles.shape = -1,

        #catch input errors
        N = len(pixelpositions)
        assert N == len(solidangles)

        #remove unit
        try:
            pixelradius + meter
        except:
            raise ValueError, 'pixel radius does not have unit: %s' % pixelradius
        
        try:
            pixelheight + meter
        except:
            raise ValueError, 'pixel height does not have unit: %s' % pixelheight

        radius = pixelradius/meter
        height = pixelheight/meter
        area = 2*radius*height

        x,y,z = pixelpositions[:,0], pixelpositions[:,1], pixelpositions[:,2]
        r2 = x*x + y*y + z*z
        import numpy
        cost = (1 - z*z/r2)**0.5
        solidangles[:] = area * cost / r2
        
        #restore shapes
        pixelpositions.shape = ppshape
        solidangles.shape = sashape
        
        return solidangles

    pass # end of SolidAngleCalculator




def test():
    calculator = SolidAngleCalculator()
    import numpy
    pixelpositions = numpy.array(
        [ [0,3.,0], [0,3,1], [3,0,0], [3,0,1] ] )
    solidangles = numpy.zeros( 4 )
    cm = units.length.cm
    pixelradius = 1*cm
    pixelheight = 1*cm
    calculator(solidangles, pixelpositions, pixelradius, pixelheight)
    assert numpy.abs( solidangles[0] - 2.222e-5 ) < 1e-7
    assert numpy.abs( solidangles[1] - 2.222e-5* (3/numpy.sqrt(10.))**3 ) < 1e-7
    assert numpy.abs( solidangles[2] - solidangles[0] ) < 1e-10
    assert numpy.abs( solidangles[3] - solidangles[1] ) < 1e-10
    return
    


def main():
    test()
    return


if __name__ == '__main__' : main()


# version
__id__ = "$Id$"

# End of file 
