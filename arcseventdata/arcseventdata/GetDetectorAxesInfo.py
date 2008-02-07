#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


## Get detector axes.
## For each detector axis, we need axis name and ids. 
##   For example: 'detectorID', [1, 2, ..., 100]


def getDetectorAxes(instrument):
    'get a list of detector axes of the given instrument'
    from histogram import axis
    return [axis( name.lower() + 'ID', ids )
            for name, ids in getDetectorAxesInfo( instrument) ]


def getDetectorAxesInfo( instrument ):
    'get info of detector axes of the given instrument'
    return GetDetectorAxesInfo().render( instrument )


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



# version
__id__ = "$Id$"

#  End of file 
