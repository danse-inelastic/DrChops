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


from Connectable import Connectable

import dsm


import journal
jrnltag = 'Composite'
warning = journal.warning( jrnltag )

class AmbiguousComponentSpecifier(Exception): pass


class Composite(Connectable):


    '''Support of connection of pyre components
    with a data-stream model.

    Requirements of components to be connected in the model:

      - Have methods getOutput and setInput to get outputs and set
        inputs.
    '''


    class Inventory(Connectable.Inventory):

        import pyre.inventory

        pass

    # an example of connections
    #connections = pyre.inventory.list(
    #    'connections', default = \
    #    ['tofWindowSelector:tofWind->tofWindow:tibgRemover',
    #     'dataSource:Idpt->maskApplyer->tibgRemover->normalizer->calibrator')
    #     'maskGenerator->mask:Nomalizer',
    #     'maskFromVanadiumdana->operand1:maskadder',
    #     'maskFromUser->operand2:maskadder',
    #     'maskAdder->mask:maskApplyer',
    #     ]


    def __init__(self, name, facility='Composite'):
        Connectable.__init__(self, name, facility)
        return


    def _update(self):
        
        components = {}
        for facname in self.inventory.facilityNames():
            components[ facname ]  = self.inventory.getTraitValue( facname )
            continue
        
        connections = self.connections
        
        composite = dsm.composite( components, connections )
        composite.sockets = self.sockets
        composite._inputs = self._inputs
        composite._update()
        self._outputs = composite._outputs
        return 


    def _configure(self):
        Connectable._configure(self)
        #should the following codes belong to __init__
        #or other stage of the life cycle of this component?
        #it is not clear to me yet.
        connections = self.__class__.connections
        connections = [tostr(c) for c in connections ]
        #print connections
        self.connections = connections
        return


    def _init(self):
        Connectable._init(self)
        return

    pass # end of Composite


def tostr( s ):
    if isinstance(s, str): return s
    import types	
    if isinstance(s, types.UnicodeType): return s.encode()
    raise NotImplementedError , "do't know how to deal with %s" %(
        s , )


def main():
    from Connectable import Connectable
    class Adder(Connectable):

        sockets = {
            'in': [ 'operand1', 'operand2' ],
            'out': ['return'],
            }
        def _update(self):
            inputs = self._inputs
            self._outputs['return'] = inputs['operand1'] + inputs['operand2']
            return
        pass
        
    class Multiplier(Connectable):

        sockets = {
            'in': [ 'operand1', 'operand2' ],
            'out': ['return'],
            }
        def _update(self):
            inputs = self._inputs
            self._outputs['return'] = inputs['operand1'] * inputs['operand2']
            return
        pass

    class DSMExample(Composite):

        sockets = {
            'in': [ '1','2','3' ],
            'out': [ 'return' ],
            }

        connections = [
            'self:1->operand1:adder',
            'self:2->operand2:adder',
            'self:3->operand1:multiplier',
            'adder:return->operand2:multiplier',
            'multiplier:return->return:self',
            ] 
        
        class Inventory(Composite.Inventory):

            import pyre.inventory as pinv
            
            adder = pinv.facility(
                'adder',
                default = Adder('adder', 'binary operator') )

            multiplier = pinv.facility(
                'multiplier',
                default = Multiplier('multiplier', 'binary operator') )
            pass


        pass # end of DSMExample
            
    
    from pyre.applications.Script import Script

    class Test(Script):

        class Inventory(Script.Inventory):

            import pyre.inventory as pinv
            dsm = pinv.facility( 'dsm', default = DSMExample('example') )
            pass # end of Inventory


        def __init__(self):
            Script.__init__(self, 'test')
            return
        

        def main(self):
            dsm = self.inventory.dsm
            warning.activate()
            
            dsm.setInput( '1', 5 )
            dsm.setInput( '2', 6 )
            dsm.setInput( '3', 7 )
            assert dsm.getOutput( 'return' )==(5+6)*7
            return

        pass # end of Test

    Test().run()
    return

warning.deactivate()


if __name__ == '__main__': main()
        

# version
__id__ = "$Id$"

# End of file 
