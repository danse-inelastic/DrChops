#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Composite import Composite as base


class Step1(base):


    '''Step #1 of preprocessing

    This preprocessor applies a detector mask to the input histogram,
    removes time-independent background, and then normalizes the
    hitogram by neutron flux.
    '''


    sockets = {
        'in': [ 'run', 'mask' ],
        'out': [ 'Idpt' ],
        }


    connections = [
        'self:mask->mask:maskApplyer',
        'self:mask->mask:tibgRemover',
        'self:run->run:normalizer',
        'self:run->run:IdptExtractor:Idpt->'\
        'Idpt:maskApplyer:Idpt->'\
        'histogram:tibgRemover:histogram->'\
        'histogram:normalizer:histogram->Idpt:self',
        ] 


    class Inventory(base.Inventory):

        import pyre.inventory as pinv
        
        f = pinv.facility

        from NormalizerUsingMonitorData import NormalizerUsingMonitorData as Normalizer
        normalizer = f('normalizer', default = Normalizer() )
        normalizer.meta['opacity'] = 10

        from IdptExtractor import IdptExtractor as IE
        IdptExtractor = f('IdptExtractor', default = IE() )
        IdptExtractor.meta['opacity'] = 100

        from ApplyMask import ApplyMask
        maskApplyer = f( 'maskApplyer', default = ApplyMask () )
        maskApplyer.meta['opacity'] = 1000

        from TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as Remover
        tibgRemover = f( 'tibgRemover', default = Remover() )
        tibgRemover.meta['importance'] = 100
        
        pass # end of Inventory


    def __init__(self, name='Preprocess_Step1' ):
        base.__init__(self, name)
        return

    pass # end of Step1
        


# version
__id__ = "$Id$"

# End of file 
