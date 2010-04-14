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


## FacilityFrontEnd
## FacilityFrontEnd is a proxy for facility and components that
## fullfill the interface requirements of the facility.
##
## This class cannot be used on any python class. The requirements
## are
##  1. The classes that can be wrapped into one front end must
##     comply to one interface. For example, at the end of this module
##     you can find a test method where "Sin" and "Cos" functors
##     are two classes having exactly the same interface.
##  2. The __init__ method of each class must have all parameters
##     defined as keywords.


def docstr( Facility ):
    
    facility = Facility.lower()
    
    enginehint = '''
This is a front end for facility "%s". For easier explanation,
here we assume that we have an instance of "%s" named "%s".

For more specific help about the current engine of this facility,
please run

    %s.help()
''' % (Facility, Facility, facility, facility)
    
    generalhelp = '''
General documentation for "%s" facility

    To create a new instance of %s,

      %s2 = %s.copy()
    
    To see what other engines are available for this %s, run

      %s.engines()

    To see what a particular underlying engine is and what it
    can do for you,

      %s.help( engine_name )

    To reconstruct the current engine,

      %s.reconstruct( *args, **kwds )

    To change this %s to use a different engine:

      %s.select( name, *args, **kwds)
    ''' % \
    tuple( [Facility, Facility, facility, facility] + [ facility ] * 6  )
    
    doc = enginehint + generalhelp
    return doc


class FacilityFrontEndCurator(type):
    

    def __init__(klass, name, bases, dict):
        import sys
        vinfo = sys.version_info
        if vinfo[0] == 2:
            if vinfo[1] <= 5:
                type.__init__(name, bases, dict)
            else:
                type.__init__(klass, name, bases, dict)
        else:
            raise NotImplementedError

        doc = docstr( name )
        klass.__doc__ = doc
        
        return

    pass #end of FacilityFrontEndCurator



class Helper:

    def __call__( self, klass, interface ):
        '''build a help page for the given klass
        only the methods in the interface are exposed.
        '''
        class t:
            pass
        klsname = klass.__name__
        newklsname = "%sInterface" % klsname
        cmd = '''
class %s: pass
t = %s''' % (newklsname, newklsname)
        exec cmd
        t.__doc__ = klass.__doc__
        for method in interface:
            def f(self, *args, **kwds): return
            f.__doc__ = getattr( klass, method ).__doc__
            setattr(t, method, f)
            continue
        return help( t )

    pass


class FacilityFrontEnd(object):

    # this will be filled up with engine factories that can
    # fullfill the requirements of the facility encapsulated
    # by this front end.
    engineFactories =  {} 

    # this should be a description of interface
    # currently it is a list of methods.
    interface = []

    # one-line description of the facility
    onelinehelp = ''

    def __init__( self ):
        self._buildInterface()
        self._engine  = None
        self._initargs = {} # dictionary of { engine:initialization arguments  }
        return


    def copy(self):
        ret = self.__class__()
        currentEngine =  self.currentEngine()
        ret.select( currentEngine )
        return ret 


    def help(self, engineName = None):
        '''help(): help message for the current engine
        help(engineName): help message for the given engine
        '''
        h = Helper()
        interface = self.interface + ['reconstruct']
        if engineName is None:
            Engine = self._engine.__class__
        else:
            Engine = self.engineFactories[ engineName ]
            pass
        self._install_dummy_reconstruct_method( Engine )
        h( Engine, interface )
        return


    def currentEngine(self):
        '''return name of the engine that is currently in use'''
        return self._engineName
    

    def engines(self):
        '''list engine factories'''
        return self.engineFactories.keys()


    def registerEngineFactory(self, name, factory):
        '''register a new engine factory'''
        self.engineFactories[name] = factory
        return 


    def select(self, name, **kwds):
        '''select a new engine

        name: name of the new engine type
        *args, **kwds: arguments and keywords for the new engine factory
        '''
        self._checkName( name )
        
        savedkwds = self._initargs.get( name )
        if savedkwds is None: savedkwds = self._initargs[name] = {}
        savedkwds.update( kwds ) # savedkwds are now updated 
        
        engine = self.engineFactories[name]( **savedkwds )
        self._setEngine( name, engine )
        return self

    
    def parameters(self):
        '''return the parameters set for the  current engin'''
        return self._initargs.get( self.currentEngine() )


    def reconstruct(self, *args, **kwds):
        '''reconstruct the current engine using new parameters
        '''
        self.select(self._engineName, *args, **kwds )
        return


    def _checkName(self, engine):
        if engine not in self.engineFactories:
            raise ValueError , \
                  "%s is not a registerd engine for facility %s" % (
                engine, self.__class__.__name__)
        return 


    def _setEngine(self, name, engine):
        self._engineName = name
        self._engine = engine

        Engine = engine.__class__
        self._install_dummy_reconstruct_method( Engine )
        return


    def _install_dummy_reconstruct_method(self, Klass):
        if Klass.__dict__.get('reconstruct'): return
        global _install_dummy_reconstruct_method
        _install_dummy_reconstruct_method( Klass )
        return


    def _buildInterface(self):
        if self.__class__.__dict__.get('_interfaceBuilt'): return
        for method in self.interface:
            methoddef = '''
def methodproxy (self, *args, **kwds):
    klass = self._engine.__class__
    t = klass.%s
    return t(self._engine, *args, **kwds)
''' % (method,)
            exec methoddef 
            setattr(self.__class__, method, methodproxy )

            continue
        setattr(self.__class__, '_interfaceBuilt', True )
        return
        

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except:
            assert self._engine is not None, "no engine for facility %s" % (
                self.__class__.__name__ )
            return getattr(self._engine, key)
        raise "should not reach here"

    __metaclass__ = FacilityFrontEndCurator

    pass # end of FacilityFrontEnd


def _install_dummy_reconstruct_method(Klass):
    if Klass.__dict__.get('reconstruct'): return
        
    def reconstruct(self, *args,**kwds):
        raise NotImplementedError , "User should use the facilityFrontEnd's reconstruct method, not engine's"
    initdoc = Klass.__init__.__doc__ or ''
    reconstruct.__doc__ = initdoc.replace(
        '__init__', 'reconstruct' )
        
    setattr( Klass, 'reconstruct', reconstruct)
    return


def methoddoc( name, method, indent ):
    doc = method.__doc__
    if len(doc): oneliner = doc.splitlines()[0]
    else: oneliner = ''
    return '%s%s: %s\n' % (indent, name, doc)


from FunctorFromFunction import FunctorFromFunction


__all__ = ['FacilityFrontEnd', 'FunctorFromFunction' ]

            
def test():

    from math import sin, cos
    
    class Sin:

        '''sin functor

        This is a simple toy functor. This functor evaluates
        the following function:

          sin(ax + b)

        '''

        def __init__(self, a=1,b=0):
            ''' __init__(a,b) --> Create functor with parameter a and b'''
            self._a = a
            self._b = b
            return

        def __call__(self, x):
            '__call__(x): return value of the functor sin(ax+b)'
            a = self._a
            b = self._b
            return sin( a*x + b )

        pass # end of Sin


    class Cos:

        'cos functor'

        def __init__(self, a=1, b=0):
            self._a = a
            self._b = b
            return

        def __call__(self, x):
            a = self._a
            b = self._b
            return cos( a*x + b )

        pass # end of Cos

    #create new facility front end class
    class Functor(FacilityFrontEnd):

        engineFactories = FacilityFrontEnd.engineFactories.copy()
        interface = [
            '__call__',
            ]
        
        pass

    #create new facilty front end instance
    functor = Functor( )
    #register classes into the front end
    #these classes will be available to any new "front-end" instance
    functor.registerEngineFactory( 'sin', Sin )
    functor.registerEngineFactory( 'cos', Cos )

    #must select an engine first
    a, b = 1., 0.
    functor.select( 'sin', a=a,b=b )
    x = 9.9
    assert functor( x ) == sin(a*x+b)

    #test of selecting new engine
    functor.select( 'cos', a=a, b=b )
    assert functor( x ) == cos(a*x+b)

    #test of change parameters
    a, b = 3.2, 1.1
    functor.reconstruct( a=a, b=b )
    assert functor( x ) == cos(a*x+b)

    #test of change 1 parameter (instead of all parameters)
    b = 0.3
    functor.reconstruct( b=b )
    assert functor( x ) == cos(a*x+b)

    #change engine back
    functor.select( 'sin', a=a, b=b)
    assert functor( x ) == sin(a*x+b)

    #test helpers
    help(functor)
    functor.help()
    functor.help('sin')
    help(functor.reconstruct)

    #test method "engines"
    print functor.engines()

    #test multiple instances of "front-end"
    functor1 = Functor()
    assert functor1 is not functor
    assert len(functor1.engines()) == 2

    #test method "copy"
    functor2 = functor.copy()

    functor2.reconstruct( a=1., b= 1.)

    #test dynamically add more classes to the "front-end"
    class Tan:

        'tan functor'

        def __init__(self, a=1, b=0):
            self._a = a
            self._b = b
            return

        def __call__(self, x):
            a = self._a
            b = self._b
            return tan( a*x + b )

        pass # end of Tan

    functor2.registerEngineFactory( 'tan', Tan )
    functor2.help( 'tan' )

    #test method "currentEngine"
    functor2.select( 'tan' )
    print functor2.currentEngine()
    assert functor2.currentEngine() == "tan"
    return


def testHelper():
    class A:
        'class A'
        def a(self):
            'method A.a'
            return
        pass
    h = Helper()
    return h( A, ['a'] )


def main():
    testHelper()
    test()
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
