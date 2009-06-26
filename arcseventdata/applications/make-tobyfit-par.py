#!/usr/bin/env python


import journal
info = journal.info('make-merlin-par')

def getpixelinfo(ARCSxml):
    info.log('parsing acrs xml: %s' % ARCSxml)
    from instrument.nixml import parse_file
    instrument = parse_file(ARCSxml)
    
    info.log('getting detector axes')
    from arcseventdata.GetDetectorAxesInfo import getDetectorAxes
    detaxes = getDetectorAxes(instrument)

    npacks, ndetsperpack, npixelsperdet = [axis.size() for axis in detaxes]

    info.log('getting pixel radii and heights')
    from arcseventdata.getpixelsizes import getpixelsizes
    radii, heights = getpixelsizes(
        instrument, npacks, ndetsperpack, npixelsperdet)
    widths = radii*2.

    info.log('getting pixel L2, phis, psis')
    from arcseventdata import getinstrumentinfo
    ii = getinstrumentinfo(ARCSxml)

    dists = ii['dists']
    phis = ii['phis']
    psis = ii['psis']
     
    from reduction.units import length, angle
    dists = dists.I
    phis = phis.I
    psis = psis.I

    dists.shape = phis.shape = psis.shape = widths.shape = heights.shape = -1,
    return dists, phis, psis, widths, heights


def getpixelinfo_mergedpixels(ARCSxml, pixelresolution):
    npixels = 128
    assert npixels%pixelresolution==0
    
    from arcseventdata.combinepixels import combinepixels, geometricInfo, geometricInfo_MergedPixels
    from histogram import axis
    pixelaxis = axis('pixelID', range(0, 128, pixelresolution))

    phi_p, psi_p, dist_p, sa_p, dphi_p, dpsi_p = combinepixels(ARCSxml, pixelaxis, pixelresolution)
    positions, radii, heights = geometricInfo(ARCSxml)
    positions, radii, heights = geometricInfo_MergedPixels(positions, radii, heights, pixelresolution)

    widths = radii*2
    
    phis = phi_p.I
    psis = psi_p.I
    dists = dist_p.I
    
    dists.shape = phis.shape = psis.shape = widths.shape = heights.shape = -1,
    return dists, phis, psis, widths, heights


def writePar(stream, dists, phis, psis, widths, heights):
    info.log('writing to par file')
    n = len(dists)
    assert n==len(phis) and n==len(psis) and n==len(widths) and n==len(heights)

    def format(f):
        return '%8.3f' % f
    stream.write(str(n)+'\n')
    for line in zip(dists, phis, psis, widths, heights):
        s = ''.join(map(format, line))
        s += '\n'
        stream.write(s)
        continue

    return


from pyre.applications.Script import Script

class App(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory
        arcsxml = pyre.inventory.str('x', default='ARCS.xml')
        outfile = pyre.inventory.str('o', default='ARCS.par')
        resolution = pyre.inventory.int('r', default=1)

    def main(self):
        arcsxml = self.inventory.arcsxml
        outfile = self.inventory.outfile
        resolution = self.inventory.resolution

        if resolution == 1:
            dists, phis, psis, widths, heights = getpixelinfo(arcsxml)
        else:
            dists, phis, psis, widths, heights = getpixelinfo_mergedpixels(arcsxml, resolution)
        writePar(open(outfile, 'w'), dists, phis, psis, widths, heights)
        return



def main():
    info.activate()
    app = App('make-merlin-par')
    app.run()
    return

if __name__ == '__main__': main()

    
