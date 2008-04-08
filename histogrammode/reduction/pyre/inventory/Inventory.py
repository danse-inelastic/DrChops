#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



class ObservableAdapter:

    '''Adapter to make an inventory observable
    '''


    def registerObserver(self, observer):
        registry = self._getObserverRegistry()
        if observer not in registry: registry.append( observer )
        return


    def notifyObservers(self):
        for observer in self._getObserverRegistry():
            observer.update( self )
            continue
        return


    def _getObserverRegistry(self):
        try: self._observers
        except: self._observers = []
        return self._observers
    
    pass



from pyre.inventory.Inventory import Inventory

class ObserveTraits( ObservableAdapter ):

    '''Make inventory observable.

Description:
  If any trait in the observed inventory changes, 
  every observer of this inventory will be notified.
  '''

    def _initializeTraitValue(self, name, value, locator):
        ret = Inventory._initializeTraitValue( self, name, value, locator )
        self.notifyObservers()
        return ret

    def _setTraitValue( self, name, value, locator ):
        ret = Inventory._setTraitValue(self, name, value, locator )
        self.notifyObservers()
        return

    pass # end of ObserveTrait



class ObserveTrait:
    
    '''Make inventory observable.

Description:
  An observable can be reigistered to a specific trait by
    inventory.registerTraitObserver( traitname, observer )
  When a change happens to a trait, any observer that is
  registered for that particular trait will be notified.
  '''

    def registerTraitObserver(self, traitname, observer):
        registry = self._getTraitObserverRegistry(traitname)
        if observer not in registry: registry.append( observer )
        return

    
    def _initializeTraitValue(self, name, value, locator):
        ret = Inventory._initializeTraitValue( 
            self, name, value, locator )
        registry = self._getTraitObserverRegistry(name)
        for observer in registry: observer.update( value )
        return ret


    def _setTraitValue( self, name, value, locator ):
        ret = Inventory._setTraitValue(self, name, value, locator )
        registry = self._getTraitObserverRegistry(name)
        for observer in registry: observer.update( value )
        return ret 


    def _getTraitObserverRegistry(self, name):
        try: self._trait_observers
        except: self._trait_observers = {}
        reg = self._trait_observers.get ( name )
        if reg is None: reg = self._trait_observers[name] = []
        return reg
    
    pass # end of ObserveTrait




def test():
    from pyre.applications.Script import Script
    
    class Test(Script):

        class Inventory( ObserveTrait, Script.Inventory ):

            import pyre.inventory as inv
            
            a = inv.str( 'a', default = 'hello')
            
            pass # end of Inventory


        def __init__(self, name = "Test" ):
            
            Script.__init__(self,name)
            self.inventory.registerTraitObserver( 'a', self )
            return


        def main(self):
            self.inventory.a = 'hi'
            assert self.greeting == 'hi'
            return


        def update(self, value):
            self.greeting = value
            return

        pass # end of Test

    test = Test()
    test.run()
    return




def test2():
    from pyre.applications.Script import Script
    
    class Test(Script):

        class Inventory( ObserveTraits, Script.Inventory ):

            import pyre.inventory as inv
            
            a = inv.str( 'a', default = 'hello')
            
            pass # end of Inventory


        def __init__(self, name = "Test" ):
            
            Script.__init__(self,name)
            self.inventory.registerObserver( self )
            return


        def main(self):
            self.inventory.a = 'hi'
            assert( self.inventory.a == self.greeting )
            return


        def update(self, inventory):
            self.greeting = self.inventory.a
            return

        pass # end of Test

    test = Test()
    test.run()
    return


if __name__ == '__main__':
    test()
    test2()


# version
__id__ = "$Id$"

# End of file 
