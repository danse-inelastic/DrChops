#!/usr/bin/env python

def compare(h1, h2, decimal=6):
    if len(h1.axes()) != len(h2.axes()):
        return "different axes"

    if h1.shape() != h2.shape():
        return "shape not match: %s != %s" % (h1.shape(), h2.shape())

    # compare each axis
    # ...
    if not equalArray(h1.I, h2.I, decimal=decimal):
        return "intensity not match"

    if not equalArray(h1.E2, h2.E2, decimal=decimal):
        return "errors not match"
    
    return


from numpy.testing import assert_array_almost_equal
import numpy as np
def equalArray(a1, a2, decimal=6):
    if a1.shape != a2.shape: return False
    try:
        assert_array_almost_equal(a1, a2, decimal=decimal)
        return True
    except:
        pass
    
    diff = a1 - a2
    m = diff != 0.
    mdiff = diff[m]

    # the places where there are difference should be only a small number 
    # of array elements
    if mdiff.size*1./a1.size > 0.01: return False
    
    # the sum of absolute differences is smaller than the sum of absolute intensities
    if np.abs(mdiff).sum()*1./np.abs(a1).sum() > 0.01: return False
    return True


def test1():
    assert equalArray(np.arange(10), np.arange(10))
    assert not equalArray(np.arange(10), np.arange(11))
    assert not equalArray(np.arange(10), np.arange(1,11))
    
    a1 = np.arange(0., 10., 1.)
    a2 = a1.copy(); a2[3] += 1e-7
    assert equalArray(a1, a2)

    a1 = np.arange(0., 10., 1.)
    a2 = a1.copy(); a2[3] += 1e-5
    assert not equalArray(a1, a2)

    a1 = np.arange(0., 100., 1.)
    a2 = a1.copy(); a2[3] += 1e-5
    assert equalArray(a1, a2)

    a1 = np.arange(0., 100., 1.)
    a2 = a1.copy(); a2[:10] += 1e-5
    assert not equalArray(a1, a2)

    return


def main():
    import sys
    argv = sys.argv
    filenames = argv[1:]
    
    from histogram.hdf import load
    hs = [load(f) for f in filenames]
    
    r = compare(hs[0], hs[1])
    if r: raise RuntimeError, r
    else:  print 'same'
    return


if __name__ == '__main__': main()
