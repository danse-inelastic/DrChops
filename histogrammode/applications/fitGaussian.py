#!/usr/bin/env python


from pyre.applications.Script import Script

class App(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory
        filename = pyre.inventory.str('filename')

        range = pyre.inventory.str('range')


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
        
        bg, height, center, sigma1 = fit1DGaussian(h)

        from math import sqrt, log
        sigma = sigma1 / sqrt(2.)
        fwhm = 2*sqrt(2*log(2))*sigma
        for k in ['bg', 'height', 'center', 'fwhm']:
            print '* %s: %s' % (k, eval(k))
            continue
        return


def main():
    app = App('fitGaussian')
    app.run()
    return



if __name__ == '__main__': main()

