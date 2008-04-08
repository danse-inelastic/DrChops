#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved
# Jiao Lin Copyright (c) 2007 All rights reserved

def generate():
    """generate an instrument graph appropriate for testing"""
    from instrument.elements import instrument, detectorArray, detectorPack, \
         detector, moderator, monitor
    from instrument.geometers import ARCSGeometer
    
    test = Instrument.Instrument("Test")
    geometer = ARCSGeometer.Geometer()
    geometer.register( test, [0,0,0], [0,0,0])

    detArrayID = test.getUniqueID()
    detArray = DetectorArray.DetectorArray( detArrayID, test.guid())
    test.addDetectorArray( detArray)

    # make a detector pack
    dpackGuid = test.getUniqueID()
    dpack = DetectorPack.DetectorPack( dpackGuid, test.guid())
    detArray.addElement( dpack)
    geometer.register( dpack, [1.,1.,1.], [1.,1.,1.])
    dpack.setAttribute('name', 'detPack1')

    # put an LPSD in the pack
    lpsd1id = test.getUniqueID()
    detectorID = detArray.getLongDetectorID()
    lpsd1 = LPSD.LPSD( lpsd1id, dpackGuid, detectorID)
    dpack.addElement( lpsd1)
    geometer.register( lpsd1, [2.,90.0,2.0], [2.,2.,2.])
    lpsd1.setAttribute('name', 'LPSD1')

    # add some pixels to the lpsd
    for i in range(5):
        pixid = test.getUniqueID()
        pixel = LPSDPixel.Pixel( pixid, detectorID, i, 0.01, 200.0, 12.7)
        lpsd1.addElement( pixel)
        geometer.register( pixel, [i+3.0,i+3.0,i+3.0], [i+3.0,i+3.0,i+3.0])
        pixel.setAttribute( 'name', 'pixel%s' % i)

    # add a monitor
    monid = test.getUniqueID()
    monitor = Monitor.Monitor( monid, test.guid(), 'nifty', 20.0, 100.0, 100.0,
                               'testMonitor')
    geometer.register( monitor, [8.,8.,8.], [8.,8.,8.])
    test.addElement( monitor)

    # add a moderator
    modid = test.getUniqueID()
    moderator = Moderator.Moderator( modid, test.guid(), 100.0, 100.0, 100.0,
                                     'testModerator')
    # position in spherical coords (x=-14.0, y=0.0, z = 0.0)
    modPosition = [14000.0, 90.0, 180.0]
    modOrientation =  [0.0, 0.0, 0.0]
    geometer.register( moderator, modPosition, modOrientation)
    test.addModerator( moderator)

    return test, geometer


if __name__ == '__main__':

    import journal
    journal.debug("instrument.elements").activate()
    
    instrument, geometer = generate()
    from InstrumentPrinter import Printer
    printer = Printer()

    printer.render( instrument, geometer)

# version
__id__ = "$Id: generateTestInstrument.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
