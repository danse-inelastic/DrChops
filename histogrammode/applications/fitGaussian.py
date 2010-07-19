#!/usr/bin/env python


from pyre.applications.Script import Script

class App(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory
        filename = pyre.inventory.str('filename')

        range = pyre.inventory.str('range')

        errors_as_weights = pyre.inventory.bool('errors_as_weights', default=True)

        outfile = pyre.inventory.str('outfile')

        scalefactor = pyre.inventory.float('scalefactor', default = 0.)


    def main(self):
        from reduction.histCompat.Fit1DFunction import fit1DGaussian

        import histogram.hdf as hh
        from histogram.hdf.utils import getOnlyEntry
        filename = self.inventory.filename
        entry = getOnlyEntry(filename)
        h = hh.load(filename, entry)

        #
        from pyre.units import parser
        parser = parser()
        range = parser.parse(self.inventory.range)
        h = h[range]

        scalefactor = self.inventory.scalefactor
        if scalefactor:
            h *= scalefactor, 0
            
        errors_as_weights = self.inventory.errors_as_weights
        params = bg, height, center, sigma1 = fit1DGaussian(
            h, errors_as_weights=errors_as_weights)

        from math import sqrt, log
        sigma = sigma1 / sqrt(2.)
        fwhm = 2*sqrt(2*log(2))*sigma
        for k in ['bg', 'height', 'center', 'fwhm']:
            print '* %s: %s' % (k, eval(k))
            continue

        outfile = self.inventory.outfile
        if outfile:
            from reduction.histCompat.functors import Gaussian
            g = Gaussian(*params)
            x = h.axes()[0].binCenters()
            y = h.I
            y1 = g(x)
            stream = open(outfile, 'w')
            for vs in zip(x,y,y1):
                stream.write('\t'.join(map(str, vs)))
                stream.write('\n')
                continue
        return


def main():
    app = App('fitGaussian')
    app.run()
    return



if __name__ == '__main__': main()

