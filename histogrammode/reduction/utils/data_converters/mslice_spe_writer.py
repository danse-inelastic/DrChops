#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Writer(object ):

    """writer for creating data files for mslice

    In mslice

     - phi is the scattering angle
     - psi is the angle between scattering direction and principle scattering
       plane
       
    """

    phiGridTitle = "### Phi Grid"
    EGridTitle = "### Energy Grid"
    STitle = "### S(Phi,w)"
    SerrTitle = "### Errors"
    eol = '\n'

    def __init__(self):
        """ctor( ) --> mslice spe file writer"""
        return


    def write_phx( self, sa_dp, psi_dp, filename ):
        """write_phx( sa_dp, psi_dp, filename ) --> write phx file for mslice
        filename: output filename in mslice spe format
        sa_dp: scattering_angle( det, pix ) histogram
        psi_dp: psi(det, pix) histogram. psi is the azimuthal angle, or the
                angle between the scattering direction and the principle
                scattering plane
        """
        print "mslice data writer: write phx file"
        f = open(filename, 'w')

        detAxis = sa_dp.axisFromName( "detectorID" )
        ndets = detAxis.size()
        
        pxlAxis = sa_dp.axisFromName( "pixelID" )
        npxls = pxlAxis.size()

        f.write( "%s\n" % (ndets*npxls) )

        fmtstr = "%10.4f"*6 + "%10d" + '\n'
        # look at file load_phx.m of mslice package
        # twotheta, psi, dtwotheta, dpsi (all in deg) 
        col1 = 10.0; col2 = 0.0;
        counter = 0
        for detID in detAxis.binCenters():
            for pxlID in pxlAxis.binCenters():
                counter += 1
                twotheta = sa_dp[ detID, pxlID ][0]
                psi = psi_dp[ detID, pxlID ][0]
                dtwotheta = 0.5
                dpsi = 2.0
                f.write( fmtstr % ( col1, col2, twotheta, psi, dtwotheta, dpsi, counter ) )
                continue
            continue
        return


    def write_spe(self, I_dpe, phi_dp, filename): 
        """write( I_dpe, phi_dp, filename) --> write I(det,pxl,E) and phi(det,pxl) to file in mslice format
        filename: output filename in mslice spe format
        I_dpe: I(det,pix,E) histogram
        phi_dp: phi( det, pix ) histogram
        """
        print "mslice data writer: write spe file"
        f = open(filename, 'w')
        
        detAxis = I_dpe.axisFromName( "detectorID" )
        ndets = detAxis.size()
        
        pxlAxis = I_dpe.axisFromName( "pixelID" )
        npxls = pxlAxis.size()

        eAxis = I_dpe.axisFromName( "energy" )
        nes = eAxis.size()
        
        f.write( "%s %s\n" % ( ndets * npxls, nes ) )

        self._writePhiGrid( phi_dp, f )
        self._writeEGrid( eAxis, f )
        self._writeSGrid( I_dpe, f )
        return


    def _writeSGrid( self, I_dpe, fout):
        "I_dpe: I(det,pix,E) histogram"
        print "S grid"
        eAxis = I_dpe.axisFromName( "energy" )
        s = ""
        eol = self.eol
        Ina = I_dpe.data().storage().asNumarray()
        from numpy import sqrt
        Ena = sqrt(I_dpe.errors().storage().asNumarray())
        
        for detIdx, detID in enumerate(I_dpe.axisFromName("detectorID").binCenters()):
            for pxlIdx, pixelID in enumerate(I_dpe.axisFromName("pixelID").binCenters()):

                #get a slice of this (detector, pixel)
                ina = Ina[detIdx,pxlIdx]
                s += self.STitle + eol
                s += fortran_print_numbers( ina )

                ena = Ena[detIdx, pxlIdx]
                s += self.SerrTitle + eol

                s += fortran_print_numbers( ena )
                continue
            continue

        fout.write( s )
        return


    def _writeEGrid( self, eAxis, fout):
        print "Energy Grid"
        s =  self.EGridTitle + self.eol 
        es = eAxis.binBoundaries()
        s += fortran_print_numbers( es )
        fout.write(s)
        return


    def _writePhiGrid(self, phi_dp, fout):
        "phi_dp: phi(detector, pixel) histogram"
        print "Phi Grid"
        s = self.phiGridTitle + self.eol
        eol = self.eol
        
        phiMatrix = phi_dp.data().storage().asNumarray()
        phis = []
        for idx, detID in enumerate(phi_dp.axisFromName("detectorID").binCenters()):
            phis += list( phiMatrix[idx] )
            continue
        phis.append( 0.0 ) # need one extra entry. strange thing about mslice

        s += fortran_print_numbers( phis, eol = eol )
        fout.write( s )
        return

        

def fortran_print_numbers( numbers, formatStr = "%10.3f", eol = '\n'):
    "print numbers in fortran format"
    l = [formatStr % d for d in numbers]
    s = eol.join( [ ''.join(l[8*i:8*(i+1)]) for i in range(len(l)/8+1) ] )
    s += eol
    return s    


writer = Writer()


def test():
    import numpy as n
    from histogram import makeHistogram
    det = ( "detectorID", range(10) )
    pxl = ( "pixelID", range(40) )
    E   = ( "energy", n.arange( -6,6, 1.0) )
    data = n.ones( (10,40,12) )
    errs = n.ones( (10,40,12) ) * 0.5
    I_pde =  makeHistogram( "I_dpe", [det, pxl, E], data, errs)
    
    data1 = n.ones( (10,40) )
    errs1 = n.ones( (10,40) ) * 0.
    phi_dp = makeHistogram( "phi_dp", [det,pxl], data1, errs1)

    writer.write_spe( I_pde, phi_dp, "tmp.spe" )

    data2 = n.ones( (10,40) )
    errs2 = n.ones( (10,40) ) * 0.
    psi_dp = makeHistogram( "psi_dp", [det,pxl], data1, errs1)

    writer.write_phx( phi_dp, psi_dp, "tmp.phx" )
    return


if __name__ =="__main__": test()
    


# version
__id__ = "$Id: SimpleSpeReducer.py 1132 2006-09-19 17:14:07Z linjiao $"

# End of file 
