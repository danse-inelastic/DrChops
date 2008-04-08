#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import journal
warning = journal.warning('rebin')


def rebin( sourceBB, sourceData, destBB ):

    """rebin source data with source bin boundaries to a new data array
    on destination bin boundaries

    please take care we are working on bin boundaries, not bin centers

    example
    rebin( [1., 2., 4., 8.], [1.,1.,1.], [1., 3., 5., 7.] )
    """
    
    destData = [0.0 for i in range(len(destBB)-1) ]
    for i in range( len(destBB) - 1 ):
        destB1 = destBB[i]; destB2 = destBB[i+1] #boundaries
        try:
            ib1 = findIndex( destB1, sourceBB )
            ib2 = findIndex( destB2, sourceBB )
        except Exception, msg:
            warning.log( "%s:%s" % (msg.__class__,msg ) )
            continue
        if ib1 == ib2: destData[i] = (destB2-destB1)/(sourceBB[ib1+1] - sourceBB[ib1])*sourceData[ib1]
        else:
            destData[i] += (sourceBB[ib1+1] - destB1)/(sourceBB[ib1+1]-sourceBB[ib1])*sourceData[ib1]
            destData[i] += (destB2 - sourceBB[ib2])/(sourceBB[ib2+1]-sourceBB[ib2])*sourceData[ib2]
            for j in range(ib1+1, ib2): destData[i] += sourceData[j]
        continue
    return destData


def findIndex( value, array ):
    """find value in array. return the index where array[index]<value<array[index+1]
    array is increasing with index increasing
    """
    if value < array[0] or value > array[-1]: raise IndexError , "%s: Out of bound" % value
    for i, v in enumerate(array):
        if value < v : return i-1
        continue
    raise RuntimeError , "should not reach here: findIndex( %s, %s)" % (value, array)


    
def test():
    destData = rebin( [1., 2., 4., 8.], [1.,1.,1.], [1., 3., 5., 7.] )
    expected = [1.5,0.75, 0.5]
    for a,b in zip(destData, expected): assert a==b
    print "test of rebin succeeded"
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 
