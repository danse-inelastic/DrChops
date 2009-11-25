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
        self._writer_usingnparray = WriterUsingNumpyArray()
        return


    def write_phx( self, sa_p, psi_p, dphi_p, dpsi_p, filename, mask_p=None ):
        """write_phx( sa_p, psi_p, filename ) --> write phx file for mslice
        filename: output filename in mslice spe format
        sa_p: scattering_angle( ..., pix ) histogram
        psi_p: psi(..., pix) histogram. psi is the azimuthal angle, or the
                angle between the scattering direction and the principle
                scattering plane
        """
        if mask_p is not None:
            mask_p = N.array(mask_p.I, bool)
        else:
            mask_p = None
        self._writer_usingnparray.write_phx(
            sa_p.I, psi_p.I, dphi_p.I, dpsi_p.I, filename,
            mask_p = mask_p)


    def write_spe(self, I_pe, phi_p, filename, mask_p=None): 
        """write( I_pe, phi_p, filename) --> write I(...,pxl,E) and phi(...,pxl) to file in mslice format
        filename: output filename in mslice spe format
        I_pe: I(...,pix,E) histogram
        phi_p: phi( ..., pix ) histogram
        """
        if mask_p is not None:
            mask_p = N.array(mask_p.I, bool)
        else:
            mask_p = None
        eAxis = I_pe.axisFromName( "energy" )
        ebbs = eAxis.binBoundaries()
        self._writer_usingnparray.write_spe(
            ebbs, I_pe.I, I_pe.E2, phi_p.I, filename,
            mask_p = mask_p)
        return



class WriterUsingNumpyArray(object):

    """writer for creating data files for mslice

    All inputs are numpy array
    
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


    def write_phx( self, sa_p, psi_p, dphi_p, dpsi_p, filename, mask_p=None):
        """write_phx( sa_p, psi_p, filename ) --> write phx file for mslice
        filename: output filename in mslice spe format
        sa_p: scattering_angle( ..., pix ) array
        psi_p: psi(..., pix) array. psi is the azimuthal angle, or the
                angle between the scattering direction and the principle
                scattering plane
        """
        print "mslice data writer: write phx file"
        f = open(filename, 'w')

        if mask_p is not None:
            # the convention was that when mask is 1, when need to remove the pixel
            # here we need to use mask to get rid of pixels using numpy
            # array's masking capability, which requires the opposite.
            mask_p = -mask_p
            sa_p = sa_p[mask_p].copy()
            psi_p = psi_p[mask_p].copy()
            dphi_p = dphi_p[mask_p].copy()
            dpsi_p = dpsi_p[mask_p].copy()
        else:
            sa_p = sa_p.copy()
            psi_p = psi_p.copy()
            dphi_p = dphi_p.copy()
            dpsi_p = dpsi_p.copy()
        
        assert sa_p.shape == psi_p.shape
        size = sa_p.size
        f.write( "%s\n" % size)

        fmtstr = "%10.4f"*6 + "%10d" + '\n'
        # look at file load_phx.m of mslice package
        # twotheta, psi, dtwotheta, dpsi (all in deg)
        # cols 1,2,7 are redundant
        col1 = 10.0; col2 = 0.0;
        counter = 0
        
        sa_p.shape = -1
        psi_p.shape = -1
        dphi_p.shape = -1
        dpsi_p.shape = -1
        
        
        for i in range(size):
            counter += 1
            twotheta = sa_p[i]
            psi = psi_p[i]
            dtwotheta = dphi_p[i]
            dpsi = dpsi_p[i]
            f.write( fmtstr % ( col1, col2, twotheta, psi, dtwotheta, dpsi, counter ) )
            continue
        return


    def write_spe(self, ebbs, I_pe, E2_pe, phi_p, filename, mask_p=None): 
        """write( ebbs, I_pe, E2_pe, phi_p, filename) --> write I(pxl,E), IE2(pxl,E) and phi(...,pxl) to file in mslice format
        filename: output filename in mslice spe format
        ebbs: energy bin boundaries
        I_pe: I(...,pix,E) array
        E2_pe: IE2(...,pix,E) array
        phi_p: phi( ..., pix ) array
        """
        print "mslice data writer: write spe file"

        if mask_p is not None:
            # the convention was that when mask is 1, when need to remove the pixel
            # here we need to use mask to get rid of pixels using numpy
            # array's masking capability, which requires the opposite.
            mask_p = -mask_p
            I_pe = I_pe[mask_p].copy()
            E2_pe = E2_pe[mask_p].copy()
            phi_p = phi_p[mask_p].copy()
        else:
            I_pe = I_pe.copy()
            E2_pe = E2_pe.copy()
            phi_p = phi_p.copy()

        assert I_pe.shape[:-1] == phi_p.shape

        self._adjustIntensity(I_pe, E2_pe)

        f = open(filename, 'w')
        
        nes = len(ebbs)-1

        ntotpxls = phi_p.size
        
        f.write( "%s %s\n" % ( ntotpxls, nes ) )

        self._writePhiGrid( phi_p, f )
        self._writeEGrid( ebbs, f )
        self._writeSGrid( I_pe, E2_pe, ntotpxls, nes, f )
        return


    def _adjustIntensity(self, ipe, E2pe):
        #remove negative numbers
        #ipe[ipe<0]=0
        #remove nan
        ipe[N.isnan(ipe)]=0
        ipe[N.isinf(ipe)]=0

        #remove negative numbers
        E2pe[E2pe<0] *= -1
        #remove nan
        E2pe[N.isnan(E2pe)]=0        
        E2pe[N.isinf(E2pe)]=0        
        return


    def _writeSGrid(self, I_pe, E2_pe, ntotpixels, nEbins, fout):
        "I_pe: I(...,pix,E) array"
        print "S grid"
        Ina = N.array( I_pe, 'd' )
        Ina.shape = ntotpixels, nEbins
        from numpy import sqrt
        Ena = sqrt(N.array(E2_pe, 'd'))
        Ena.shape = ntotpixels, nEbins

        import arcseventdata
        s = arcseventdata.SGrid_str_numpyarray( Ina, Ena, ntotpixels, nEbins )

        fout.write(s)
        return
        

    def _writeSGrid_slow( self, I_pe, E2_pe, ntotpixels, nEbins, fout):
        "I_pe: I(...,pix,E) histogram"
        print "S grid"
        s = ""
        eol = self.eol
        Ina = N.array( I_pe, copy = 0 )
        Ina.shape = ntotpixels, nEbins
        from numpy import sqrt
        Ena = sqrt(E2_pe)
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


    def _writeEGrid( self, ebbs, fout):
        print "Energy Grid"
        s =  self.EGridTitle + self.eol 
        s += fortran_print_numbers( ebbs )
        fout.write(s)
        return


    def _writePhiGrid(self, phi_p, fout):
        "phi_p: phi(..., pixel) histogram"
        print "Phi Grid"
        s = self.phiGridTitle + self.eol
        eol = self.eol
        
        phis = N.array(phi_p, copy = 0 )
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

    sa_p = psi_p = dphi_p = dpsi_p = phi_p
    writer.write_phx(sa_p, psi_p, dphi_p, dpsi_p, "tmp.phx" )
    return

def test3():
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

    data2 = n.ones( (10,40),  int )
    errs2 = n.zeros( (10,40),  int )
    data2[:,0] = 0
    mask_p = makeHistogram( "mask_p", [det,pxl], data2, errs2)

    writer.write_spe( I_pe, phi_p, "tmp-withmask.spe", mask_p=mask_p)

    sa_p = psi_p = dphi_p = dpsi_p = phi_p
    writer.write_phx(sa_p, psi_p, dphi_p, dpsi_p, "tmp-withmask.phx" , mask_p=mask_p)
    return

def test():
    test1()
    test2()
    test3()
    return

if __name__ =="__main__": test()
    


# version
__id__ = "$Id: SimpleSpeReducer.py 1132 2006-09-19 17:14:07Z linjiao $"

# End of file 
