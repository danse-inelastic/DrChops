#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## This script reads events from event data file
## and create a histogram hdf5 file of I(h, k, l, E)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        E_params = Tuple( 'E', default = '-50,50,10.' )
        E_params.meta['tip'] = "energy bin parameters (begin, end, step). units: meV"

        h_params = Tuple( 'hh', default = '-10,10,1.' )
        h_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        k_params = Tuple( 'kk', default = '-10,10,1.' )
        k_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        l_params = Tuple( 'll', default = '-10,10,1.' )
        l_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        Ei = pinv.float( 'I', default = 60 )
        Ei.meta['tip'] = 'incident energy. unit: meV'

        ub = pinv.str('ub', default = '')
        ub.meta['tip'] = 'matrix that converts Q vector to hkl'

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def main(self):
        self.compute()
        #self.normalize()
        self.save()
        return


    def build_args(self):
        h_params = self.inventory.h_params
        k_params = self.inventory.k_params
        l_params = self.inventory.l_params
        E_params = self.inventory.E_params
        ARCSxml = self.inventory.ARCSxml
        Ei = self.inventory.Ei
        
        ub = self.inventory.ub
        if not ub: ub = ( (1., 0., 0.),
                          (0., 1., 0.),
                          (0., 0., 1.), )
        else:
            f = open(ub)
            s = f.read()
            ub = eval(s)
            ub = _matrix33(ub)
            
        emission_time = self.inventory.emission_time
        return h_params, k_params, l_params, E_params, ARCSxml, Ei, ub, emission_time
    
    
    def normalize(self):
        if self.mpiRank == 0:
            histogram = self.histogram
            self.histogram = self.inventory.engine.normalize( histogram )
        return
    
    
    def _defaults(self):
        base._defaults(self)
        from arcseventdata.parallel_histogrammers.components.IhkleHistogrammer import IhkleHistogrammer as Engine
        self.inventory.engine = Engine( )
        return


    def _init(self):
        base._init(self)
        return


    pass # end of Application


def _matrix33(m):
    assert len(m)==3
    r = []
    for e in m:
        assert len(e) == 3
        e = float(e(0)), float(e(1)), float(e(2))
        r.append(e)
        continue
    return tuple(r)


def main():
    Application('ihkle').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer4' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
