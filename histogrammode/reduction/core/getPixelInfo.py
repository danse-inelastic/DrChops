#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.core.getPixelInfo


import journal
debug = journal.debug( 'reduction.core.getPixelInfo')
warning = journal.warning( 'reduction.core.getPixelInfo')


cache1 = None
cache2 = None
def getPixelGeometricInfo( instrument, geometer, detaxes ):
    global cache1, cache2
    if cache2 is None:
        cache2 = _Cache2( 'pixelInfo', 'pixelInfo-cache' )
        pass # end if
    if cache1 is None:
        cache1 = _Cache1( 'pixelInfo' )
        pass # end if

    try:
        all = cache1.get( (instrument, geometer) )
    except:
        all = cache2.get( (instrument, geometer) )
        cache1.set( (instrument, geometer), all )
        pass

    #one histogram representattive
    h1 = all[0]
    
    #
    sliceInfo = {}; sliceable = True

    for detaxis in detaxes:
        ids = detaxis.binCenters()
        if not _isContiguousPortion( ids, h1.axisFromName( detaxis.name() ) ):
            # cannot use slice
            sliceable = False
            break
        sliceInfo[ detaxis.name() ] = ids[0], ids[-1]
        continue

    debug.log('sliceable = %s' % sliceable)
    debug.log('sliceInfo = %s' % sliceInfo)
    if sliceable: return [ h[ sliceInfo ] for h in all]
    
    #this means we have to use slow slicing
    from histogram import getSliceCopyFromHistogram
    ret = [
        getSliceCopyFromHistogram( h.name(), detaxes, h )
        for h in all ]
    debug.log("a returned histogram: %s" % ret[0] )
    return ret


def getDetectorAxes(instrument):
    'get a list of detector axes of the given instrument'
    from histogram import axis
    return [axis( name.lower() + 'ID', ids )
            for name, ids in getDetectorAxesInfo( instrument) ]


def getDetectorAxesInfo( instrument ):
    'get info of detector axes of the given instrument'
    return GetDetectorAxesInfo().render( instrument )




#implementation

from reduction.utils.MemoryCache import MemoryCache as base
class _Cache1( base ):
    def _hashableKey(self, key):
        instrument, geometer = key
        return instrument.name
    pass # _cache1

from reduction.utils.DiskCache import DiskCache as base
from ParallelComponent import ParallelComponent
class _Cache2( base, ParallelComponent ):

    instrumentxmlfmtstr = 'cached-%(name)s.xml' 

    def __init__(self, instrumentName, cachedir):
        base.__init__(self, instrumentName, cachedir )
        return


    def _hashableKey( self, key ):
        debug.log("key=%s" % (key,))
        instrument, geometer = key
        return instrument.name


    def _outdated(self, key):
        debug.log("key=%s" % (key,))
        instrument, geometer = key
        ixml = self._ixml( instrument.name )
        from instrument.nixml import render, parse
        try:
            texts = render( instrument )
        except:
            #this means we cannot render the instrument to a xml file
            #and it means the instrument and geometer
            #is not created using a hierarchy.
            #In this case, we don't know how to save instrument
            #signature, and compare old and new signatures.
            #so we just say it is always outdated
            return True
        texts = [ t.encode() for t in texts ]
        try: oldtexts = open( ixml ).read()
        except: return True
        oldtexts = oldtexts.strip().split('\n')

        new = '\n'.join(texts[:-3])
        old = '\n'.join(oldtexts[:-3])
        #print >> open('new.log','w'), new
        #print >> open('old.log','w'), old

        ret = old != new
        #print >> open("ret.log",'w'), ret
        
        #pickle.dump( oldtexts, open('old.pkl','w') )
        #pickle.dump( texts, open('new.pkl','w') )
        return ret


    def _ixml(self, instrumentname):
        debug.log("instrumentname=%s" % (instrumentname,))
        ixml = self.instrumentxmlfmtstr % {'name':instrumentname}
        ixml = os.path.join( self._path, ixml )
        return ixml


    def _dump(self, stuff, path):
        debug.log( 'stuff=%s' % (stuff,) )
        if os.path.exists(path): os.remove( path )
        #pickle.dump( stuff, open('stuff1.pkl', 'w') )
        for i, h in enumerate(stuff):
            mode = 'w'
            if i==0: mode = 'c'
            hh.dump( h, path, '/', mode)
            continue
        return


    def _makeCache(self, key, value):
        debug.log("key=%s" % (key,))
        base._makeCache(self, key, value)
        instrument, g = key
        #this is the signature of the cache
        try:
            from instrument.nixml import weave
            weave( instrument,
                   open(self._ixml( instrument.name ), 'w') )
        except:
            msg = "don't know how to create signature of instrument %s" %(
                instrument.name, )
            warning.log( msg )
            pass
        return


    def _load(self, path):
        debug.log("path=%s" % (path,))
        phi_dp = hh.load( path, 'phi' )
        #hack.pyreunit has problems
        phi_dp = _toDegrees( phi_dp )
        distance_dp = hh.load( path, 'distance' )
        solid_angle_dp = hh.load( path, 'solid_angle' )
        radius_dp = hh.load( path, 'radius' )
        pressure_dp = hh.load( path, 'pressure' )
        ret = phi_dp, solid_angle_dp, distance_dp, radius_dp, pressure_dp
        return ret


    def _compute(self, key):
        debug.log("key=%s" % (key,))
        instrument, geometer = key
        completedetaxes = getDetectorAxes( instrument )
        pickle.dump( completedetaxes, open('completeaxes.pkl','w') )
        return _DataCollector( ).render(instrument, geometer, completedetaxes)


    pass # end of _Cache
import histogram.hdf as hh
import os, pickle


def _toDegrees( phis ):
    #temp hack due to pyre.units problem
    axes = phis.axes()
    from histogram import histogram
    new = histogram( 'phi', axes, unit = 'degree' )
    from pyre.units.angle import radian
    new[{}] = phis.data().storage().asNumarray() * phis.unit() * radian, 0*radian
    return new


from pyre.units.angle import deg
from LoopUtils import DetectorVisitor
class _DataCollector(DetectorVisitor):

    def render(self, instrument, geometer, detaxes):

        from histogram import histogram
        self.phi_dp = histogram( 'phi', detaxes, unit = 'deg' )
        self.dist_dp = histogram( 'distance', detaxes, unit = 'mm')
        self.radius_dp = histogram( 'radius', detaxes, unit = 'cm')
        self.pressure_dp = histogram( 'pressure', detaxes, unit = 'atm')
        self.sa_dp = histogram( 'solid_angle', detaxes )

        DetectorVisitor.render( self, instrument, geometer )

        ret = self.phi_dp, self.sa_dp, self.dist_dp, self.radius_dp, self.pressure_dp
        del self.phi_dp, self.sa_dp, self.dist_dp, self.radius_dp, self.pressure_dp
        return ret


    def onDetector(self, detector):
        self.onElementContainer( detector )
        detectorSignature = self.detectorElementSignature()
        slice = detectorSignature + ( (), )
        
        radius = detector.shape().radius
        self.radius_dp[ slice ] = radius, 0*radius*radius

        pressure = detector.pressure()
        #print pressure
        self.pressure_dp[ slice ] = pressure, 0*pressure*pressure
        return


    def onPixel(self, pixel):

        signature = self.elementSignature( )

        geometer = self._geometer
        distance = geometer.distanceToSample( signature )

        arrindexes = self.dist_dp.values2indexes(self.detectorElementSignature())

        self.dist_dp.data()[ arrindexes ] = distance
        
        phi = geometer.scatteringAngle( signature )
        self.phi_dp.data()[ arrindexes ] = phi 

        #hack. solid angle should be registered in geometer
        self.sa_dp.data()[ arrindexes ] = 1.
        return

    pass # end




from instrument.elements.Visitor import Visitor
class GetDetectorAxesInfo(Visitor):

    def render(self, instrument):
        self._layers = []
        self._idss = []
        self._level = 0
        Visitor.render( self, instrument, None )
        ret = zip(self._layers, self._idss)
        del self._level, self._idss, self._layers
        return ret

    def onInstrument(self, instrument):
        for e in instrument: e.identify(self)
        return

    def onContainer(self, container):
        ids = [ e.id() for e in container.elements() ]
        n = len(ids)
        if self._level == len(self._idss):
            #this means this is the first time we
            #are encountered with the current detector type
            #So we should append all ids for this new layer
            #into the idss (list of ids)
            
            self._idss.append( ids )
            # we are assuming all elements are the same type
            # should we check that?
            if n>0:
                typeName = container.elements()[0].__class__.__name__
                for e in container.elements()[1:]:
                    t = e.__class__.__name__
                    if t == 'Copy': t = e.reference().__class__.__name__
                    assert t == typeName, \
                           "typename mismatch: %s, %s" % (
                        typeName, t )
                self._layers.append( typeName )
                pass
                
        elif self._level < len(self._idss):

            #This means that we have already enounter this detector
            #type, and we want to make sure all ids are consistent.

            #first we want to keep the longest list of ids
            
            if len(self._idss[self._level]) < n:
                shortids = self._idss[self._level]
                longids = self._idss[self._level] = ids
            else:
                shortids = ids
                longids = self._idss[self._level]
            #now check for consistency
            assert shortids == longids[: len(shortids)]

            # we assume that this detector system is flattenable
            typeName = self._layers[self._level] 
            for e in container.elements():
                t = e.__class__.__name__
                if t == 'Copy': t = e.reference().__class__.__name__
                assert typeName == t, \
                       "typename mismatch: %s, %s" % (
                    typeName, e.__class__.__name__ )
                continue
            pass
        else:
            raise RuntimeError , "ids: %s, level: %s, idss: %s" %(
                ids, self._level, self._idss)
        self._level += 1
        for element in container: element.identify( self )
        self._level -= 1
        return

    onDetectorSystem = onDetectorArray = onDetectorPack = onDetector = onContainer

    def doNothing(self, e): return
    onSample = onModerator = onMonitor = onGuide = onPixel = onCopy = doNothing

    pass # end of GetDetectorHierarchyDimensions



def _compareArray( arr1, arr2 ):
    ''' compare two integer arrays. if same return False.

    This function assumes the given arrays contain the same type of
    numbers.
    '''
    debug.log('arr1, arr2 = %s, %s' % (
        arr1, arr2) )
    debug.log('lengths of arr1 and arr2: %s, %s' % (
        len(arr1), len(arr2) ) )
    if len(arr1) != len(arr2): return True
    for e1, e2 in zip(arr1, arr2):
        if e1-e2 != 0*e1: return True
        continue
    return False


def _isContiguousPortion( bincenters, axis ):
    '''check whether the given list of bin centers is a contiguous
    portion of the given axis

    _isContiguousPortion([1,2,3], axis('id', range(10)) --> True
    _isContiguousPortion([1,3,4], axis('id', range(10)) --> False
    _isContiguousPortion([2,5], axis('id', [1,2,5,6]) --> True
    _isContiguousPortion([1,5], axis('id', [1,2,5,6]) --> False
    '''
    allbincenters = list(axis.binCenters())
    
    debug.log("bincenters = %s, allbincenters = %s" % (
        bincenters, allbincenters ) )
    startindex = allbincenters.index(bincenters[0])
    endindex = allbincenters.index(bincenters[-1]) + 1
    return not _compareArray(
        allbincenters[ startindex: endindex ], bincenters)


def test_isContiguousPortion( ):
    from histogram import axis
    assert _isContiguousPortion([1,2,3], axis('ID', range(10))) == True 
    assert _isContiguousPortion([1,3,4], axis('ID', range(10))) == False
    assert _isContiguousPortion([2,5], axis('ID', [1,2,5,6])) == True
    assert _isContiguousPortion([1,5], axis('ID', [1,2,5,6])) == False
    return


def main():
    test_isContiguousPortion()
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
