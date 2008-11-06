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


"""
Difficulties of writing mslice files:

spe
 * Make sure data don't have nan or inf.
 * Use E (scientific) format for output S and ERR.
   sth like: +3.142E+00
"""


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


    def write_phx( self, sa_p, psi_p, filename ):
        """write_phx( sa_p, psi_p, filename ) --> write phx file for mslice
        filename: output filename in mslice spe format
        sa_p: scattering_angle( ..., pix ) histogram
        psi_p: psi(..., pix) histogram. psi is the azimuthal angle, or the
                angle between the scattering direction and the principle
                scattering plane
        """
        print "mslice data writer: write phx file"
        f = open(filename, 'w')

        assert sa_p.shape() == psi_p.shape()
        size = sa_p.size()
        f.write( "%s\n" % size)

        fmtstr = "%10.4f"*6 + "%10d" + '\n'
        # look at file load_phx.m of mslice package
        # twotheta, psi, dtwotheta, dpsi (all in deg)
        # cols 1,2,7 are redundant
        col1 = 10.0; col2 = 0.0;
        counter = 0
        
        sa_arr = N.array( sa_p.data().storage().asNumarray(), copy = 0 )
        sa_arr.shape = -1,

        psi_arr = N.array( psi_p.data().storage().asNumarray(), copy = 0 )
        psi_arr.shape = -1,
        
        for i in range(size):
            counter += 1
            twotheta = sa_arr[i]
            psi = psi_arr[i]
            dtwotheta = 0.5 #  ???
            dpsi = 2.0 # ???
            f.write( fmtstr % ( col1, col2, twotheta, psi, dtwotheta, dpsi, counter ) )
            continue
        return


    def write_spe(self, I_pe, phi_p, filename): 
        """write( I_pe, phi_p, filename) --> write I(...,pxl,E) and phi(...,pxl) to file in mslice format
        filename: output filename in mslice spe format
        I_pe: I(...,pix,E) histogram
        phi_p: phi( ..., pix ) histogram
        """
        print "mslice data writer: write spe file"
        
        assert I_pe.shape()[:-1] == phi_p.shape()

        #make a copy so we can change it
        I_pe = I_pe.copy()
        self._adjustIntensity(I_pe)
        
        f = open(filename, 'w')
        
        eAxis = I_pe.axisFromName( "energy" )
        nes = eAxis.size()

        ntotpxls = phi_p.size()
        
        f.write( "%s %s\n" % ( ntotpxls, nes ) )

        self._writePhiGrid( phi_p, f )
        self._writeEGrid( eAxis, f )
        self._writeSGrid( I_pe, ntotpxls, nes, f )
        return


    def _adjustIntensity(self, ipe):
        import numpy as N

        iarr = ipe.I
        #remove negative numbers
        iarr[iarr<0]=0
        #remove nan
        iarr[N.isnan(iarr)]=0
        iarr[N.isinf(iarr)]=0

        e2arr = ipe.E2
        #remove negative numbers
        e2arr[e2arr<0]=0
        #remove nan
        e2arr[N.isnan(e2arr)]=0        
        e2arr[N.isinf(e2arr)]=0        

        return


    def _writeSGrid(self, I_pe, ntotpixels, nEbins, fout):
        "I_pe: I(...,pix,E) histogram"
        print "S grid"
        eAxis = I_pe.axisFromName( "energy" )
        Ina = N.array( I_pe.data().storage().asNumarray(), 'd' )
        Ina.shape = ntotpixels, nEbins
        from numpy import sqrt
        Ena = sqrt(N.array(I_pe.errors().storage().asNumarray(), 'd'))
        Ena.shape = ntotpixels, nEbins

        import arcseventdata
        s = arcseventdata.SGrid_str_numpyarray( Ina, Ena, ntotpixels, nEbins )

        fout.write(s)
        return
        

    def _writeSGrid_slow( self, I_pe, ntotpixels, nEbins, fout):
        "I_pe: I(...,pix,E) histogram"
        print "S grid"
        eAxis = I_pe.axisFromName( "energy" )
        s = ""
        eol = self.eol
        Ina = N.array( I_pe.data().storage().asNumarray(), copy = 0 )
        Ina.shape = ntotpixels, nEbins
        from numpy import sqrt
        Ena = sqrt(I_pe.errors().storage().asNumarray())
        Ena.shape = ntotpixels, nEbins

        for i in range(ntotpixels):
            if i%100 == 0: print i
            #get a slice of this pixel
            ina = Ina[i]
            s += self.STitle + eol
            s += fortran_print_numbers( ina )

            ena = Ena[i]
            s += self.SerrTitle + eol
            s += fortran_print_numbers( ena )
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


    def _writePhiGrid(self, phi_p, fout):
        "phi_p: phi(..., pixel) histogram"
        print "Phi Grid"
        s = self.phiGridTitle + self.eol
        eol = self.eol
        
        phis = N.array( phi_p.data().storage().asNumarray(), copy = 0 )
        phis.shape = -1,
        phis = list(phis)
        phis.append( 0.0 ) # need one extra entry. strange thing about mslice

        s += fortran_print_numbers( phis, eol = eol )
        fout.write( s )
        return

        

def fortran_print_numbers( numbers, formatStr = "%10.3f", eol = '\n'):
    "print numbers in fortran format"
    l = [formatStr % d for d in numbers]
    if len(l)==0: raise ValueError, "number list is empty"
    s = eol.join( [ ''.join(l[8*i:8*(i+1)]) for i in range((len(l)-1)/8+1) ] )
    s += eol
    return s    


import numpy as N

writer = Writer()


def test1():
    eol = Writer.eol
    
    s1 = fortran_print_numbers( range(3) )
    assert s1[-1] == eol and s1[-2]!=eol

    s1 = fortran_print_numbers( range(8) )
    assert s1[-1] == eol and s1[-2]!=eol

    s1 = fortran_print_numbers( range(15) )
    assert s1[-1] == eol and s1[-2]!=eol

    return

def test2():
    import numpy as n
    from histogram import makeHistogram
    det = ( "detectorID", range(10) )
    pxl = ( "pixelID", range(40) )
    E   = ( "energy", n.arange( -6,6, 1.0) )
    data = n.ones( (10,40,12) )
    errs = n.ones( (10,40,12) ) * 0.5
    I_pe =  makeHistogram( "I_pe", [det, pxl, E], data, errs)
    
    data1 = n.ones( (10,40) )
    errs1 = n.ones( (10,40) ) * 0.
    phi_p = makeHistogram( "phi_p", [det,pxl], data1, errs1)

    writer.write_spe( I_pe, phi_p, "tmp.spe" )

    data2 = n.ones( (10,40) )
    errs2 = n.ones( (10,40) ) * 0.
    psi_p = makeHistogram( "psi_p", [det,pxl], data1, errs1)

    writer.write_phx( phi_p, psi_p, "tmp.phx" )
    return

def test():
    test1()
    test2()
    return

if __name__ =="__main__": test()
    


# version
__id__ = "$Id: SimpleSpeReducer.py 1132 2006-09-19 17:14:07Z linjiao $"

# End of file 
