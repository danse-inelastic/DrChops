#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



class PseudoSingleton(object):

    def __new__(cls, *args, **kwds):
        its = cls.__dict__.get("__its__")
        # some time we need to reinitialize the instance
        reset = False
        if kwds.has_key('reset'): reset = True; del( kwds['reset'] )
        key = args, totuples( kwds )
        if its is None: its = cls.__its__ = {}

        it = its.get(key)
        if it is None:
            its[key] = it = object.__new__( cls )
            cls.__init1__(it, *args, **kwds)
        if reset: cls.__init1__(it, *args, **kwds)
        return it


    def __init__(self, *args, **kwds):
        "should not overload this method!"
        object.__init__(self)
        return


    def __init1__(self, *args, **kwds):
        raise NotImplementedError , "This method should be reloaded to replace __init__"


    pass


def totuples( d ):
    ret = []
    for k, v in d.iteritems():
        ret.append( (k,v) )
        continue
    return tuple( ret )


def test():

    class A( PseudoSingleton ):

        def __init1__(self, a):
            self.a = a
            return

        pass

    assert A(1) is A(1)
    assert A(1) is not A(2)

    class B:
        def __init__(self, a):
            self.a = a
            return

        pass

    assert B(1) is not B(1)


    class C( PseudoSingleton ):

        def __init1__(self, a):
            self.a = a
            self.count = 0
            return

        def increase(self):  self.count += 1
        pass

    c1 = C(1)
    c2 = C(1)
    c1.increase()
    assert c2.count == 1
    c1.increase()
    assert c1 is c2
    assert c2.count == 2

    c3 = C(1, reset=1)
    assert c1 is c2
    assert c2 is c3
    assert c2.count == 0

    return


if __name__ == '__main__': test()

# version
__id__ = "$Id$"

# End of file 
