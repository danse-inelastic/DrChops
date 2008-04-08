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


from Step1 import Step1 as base

class Step1_withTibgWindowPicker(base):


    '''Step #1 of preprocessing

    This preprocessor applies a detector mask to the input histogram,
    removes time-independent background, and then normalizes the
    hitogram by neutron flux.
    '''


    connections = [
        'self:mask->mask:maskApplyer',
        'self:mask->mask:tibgRemover',
        'self:run->run:normalizer',
        'self:run->run:IdptExtractor:Idpt->Idpt:maskApplyer',
        'maskApplyer:Idpt->Idpt:TofWindowSelector',
        'TofWindowSelector:tofWindow->tofWindow:tibgRemover',
        'maskApplyer:Idpt->histogram:tibgRemover:histogram->'\
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
        IdptExtractor.meta['opacity'] = 1000

        from ApplyMask import ApplyMask
        maskApplyer = f( 'maskApplyer', default = ApplyMask () )
        maskApplyer.meta['opacity'] = 1000

        from TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as Remover
        tibgRemover = f( 'tibgRemover', default = Remover() )
        tibgRemover.meta['importance'] = 100
        tibgRemover.meta['opacity'] = 800

        from TofWindowSelector import TofWindowSelector as Selector
        TofWindowSelector = f('TofWindowSelector', factory = Selector)
        TofWindowSelector.meta['opacity'] = 1000
        
        pass # end of Inventory


    def __init__(self, name='Preprocess_Step1_withTibgWindowPicker' ):
        base.__init__(self, name)
        return

    pass # end of Step1_withTibgWindowPicker
        


# version
__id__ = "$Id$"

# End of file 
