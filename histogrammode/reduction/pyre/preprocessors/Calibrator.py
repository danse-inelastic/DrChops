#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.pyre.Calibrator
## histogram calibrator



from Connectable import Connectable as base

class Calibrator(base):

    "histogram calibrator"

    def __init__(self, name = "Calibrator" ):
        base.__init__( self, name, facility = 'Calibrator' )
        return
    

    sockets = {
        'in': ['calibration constants', 'histogram'],
        'out': ['histogram'],
        }
    

    def __call__(self, histogram, cc):
        """calibrate the given histotgram
        """
        assert len(cc.axes()) == 1 # assert cc is a histogram: cc(detID)

        detAxis = histogram.axisFromName( 'detectorID' )
        
        detIDs = detAxis.binCenters()

        print histogram.unit(), histogram.data().unit()
        from numpy import array
        for detID in detIDs:
            c = array(cc[detID]) / cc.unit()
            histogram[ {'detectorID': detID} ] /= c
            continue
        histogram /= cc.unit(), 0
        return


    def _update(self):
        cc = self._getInput('calibration constants')
        histogram = self._getInput( 'histogram' )
        self( histogram, cc )
              
        self._setOutput( 'histogram', histogram )
        return

    pass # end of Calibrator


# version
__id__ = "$Id: Calibrator.py 1270 2007-06-20 01:15:57Z linjiao $"

# End of file 
