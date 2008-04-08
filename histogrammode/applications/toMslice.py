#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \namespace reduction::applications::toMslice
# convert histograms to mslice format


from reduction.utils.pickle import load


def toMslice( I_dpe, phi_dp, psi_dp, filename ):
    from reduction.utils.data_converters.mslice_spe_writer import writer
    spefile = "%s.spe" % filename
    phxfile = "%s.phx" % filename
    writer.write_spe( I_dpe, phi_dp, spefile )
    writer.write_phx( phi_dp, psi_dp, phxfile )
    return


def toMslice2( I_dpe_pkl, phi_dp_pkl, psi_dp_pkl, filename, multiplier = 1.0 ):
    I_dpe = load( I_dpe_pkl )
    if multiplier == 1.0: multiplier = _calcDefaultMultiplier( I_dpe )
    I_dpe *= (multiplier,0.0)
    print "multiplier is %s" % multiplier
    phi_dp = load( phi_dp_pkl )
    psi_dp = load( psi_dp_pkl )
    toMslice( I_dpe, phi_dp, psi_dp, filename)
    return


def _calcDefaultMultiplier( I_dpe ):
    d = I_dpe.data().storage().asNumarray()
    d.shape = -1,
    from numpy import sqrt
    e = sqrt(I_dpe.data().storage().asNumarray())
    e.shape = -1,
    return 999./max( d.max(), e.max() )


from pyre.applications.Script import Script
class ToMslice(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory as inv
        I_dpe = inv.str( "I_dpe", default = "I_dpe.pkl" )
        phi_dp = inv.str( "phi_dp", default = "phi_dp.pkl" )
        psi_dp = inv.str( "psi_dp", default = "psi_dp.pkl" )
        output = inv.str( "output", default = "mslice-data" )
        multiplier = inv.float( "multiplier", default = 1.0 )
        pass # end of Inventory


    def __init__(self, name = "toMslice" ):
        Script.__init__(self, name)
        return
    

    def main(self):
        si = self.inventory
        toMslice2( si.I_dpe, si.phi_dp, si.psi_dp, si.output, si.multiplier )
        return

    pass # end of ToMslice
        

def main():
    app = ToMslice( "toMslice" )
    app.run()
    return


if __name__ == "__main__": main()



# version
__id__ = "$Id: SimpleSpeReducer.py 1159 2006-10-12 04:53:25Z linjiao $"

# End of file 

