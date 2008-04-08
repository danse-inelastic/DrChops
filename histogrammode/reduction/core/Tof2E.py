#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.Tof2E
## convert I( *, tof) to I(*, E )
##
## Please note that this rebinner is different from 
## other similar rebinners. Some rebinners rebin tof to Ei-Ef,
## some may rebin tof to Ef-Ei, etc etc
## this rebinner simply rebin tof of neutron to energy of neutron.



import journal
debug = journal.debug('Tof2E')


from reduction.histCompat.RebinTof2E import RebinTof2E
from AbstractTof2E import *


class Tof2E( AbstractTof2E ):

    '''Converts I(*, tof) to I(*,E)
    '''

    def __init__(self):
        '''__init__(): a new converter
        '''
        self.rebinner = RebinTof2E( 0.0 )
        return


    def __call__(self, inHist, outHist, distances):
        '''__call__( inHist, outHist, distances )

        inHist: I(*,tof)
        outHist: I(*,E)
        distances: distance( * )
        '''
        rebinner = self.rebinner
        
        tofAxis = inHist.axisFromName('tof')
        EAxis = outHist.axisFromName( 'energy' )
        
        #temporary histogram
        from histogram import histogram
        IE = histogram( 'tmp', (EAxis,) )
        
        from reduction.LoopUtils import HistogramProcessor2
        class Processor(HistogramProcessor2):

            def onPoint(self, X):
                IE.assign(0.0)
                dist = distances[X][0]
                debug.log( "dist= %s, I(tof)=%s" %(
                    dist, inHist[X] ) )
                rebinner.setDistance( dist )
                rebinner( inHist[X], outHist[X] )
                return

            pass # end of Processor

        #axes in the input histogram minus the tof axis
        otherAxes = [ inHist.axisFromName( n ) for n in inHist.axisNameList() ]
        del otherAxes[ otherAxes.index( tofAxis ) ]
        
        processor = Processor()
        processor.run( otherAxes )
        return


# version
__id__ = "$Id$"

# End of file
