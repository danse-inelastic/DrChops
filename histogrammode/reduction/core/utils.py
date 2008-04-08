#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def computeFrequencies( l, tolerance = 1.e-10 ):
    "compute frequencies of apperance of elements in a list"

    uniqueElements = []; frequencies = []
    
    for element in l:
        
        found = None
        
        for i, uniqueElement in enumerate(uniqueElements):
            
            if abs(element-uniqueElement) <= tolerance:

                found = i, uniqueElement
                break

            continue

        if not found:
            uniqueElements.append( element )
            frequencies.append( 1 )
            continue

        #
        frequencies[i] += 1

        i, uniqueElement = found
        while i > 0 and frequencies[i] > frequencies[i-1] :
            #swap i-1, i
            swap( frequencies, i-1, i )
            swap( uniqueElements, i-1, i )
            i -= 1
            continue
        
        continue


    return uniqueElements, frequencies


def swap( l, i,j ):
    "swap element i and j in list l"
    t = l[i]
    l[i] = l[j]
    l[j] = t
    return



def testComputeFrequencies( ):
    l = [0., 0., 2., 1., 2., 3., 4., 2., ]
    assert computeFrequencies( l ) == ([2.0, 0.0, 1.0, 3.0, 4.0], [3, 2, 1, 1, 1])
    return


def test():
    testComputeFrequencies()
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 
