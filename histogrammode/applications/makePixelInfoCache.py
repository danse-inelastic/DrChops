#!/usr/bin/env python

def run(instrumentxml):
    from instrument.nixml import parse_file
    instrument = parse_file( instrumentxml )
    geometer = instrument.geometer

    from reduction.core.getPixelInfo import getPixelGeometricInfo, getDetectorAxes
    detaxes = getDetectorAxes( instrument )
    getPixelGeometricInfo( instrument, geometer, detaxes )
    return


def main():
    import sys
    xml = sys.argv[1]
    run( xml )
    return

if __name__ == '__main__' : main()
