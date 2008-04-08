#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#





from pyre.applications.Script import Script as base



class PowderReductionApp(base):


    class Inventory( base.Inventory ):
        
        import pyre.inventory as inv

        from reduction.pyre.PowderReduction import PowderReduction as PRComp
        reducer = inv.facility('reducer', factory= PRComp)
        reducer.meta['tip'] = "Reduction Engine"

        pass #


    def __init__(self, name='PowderReductionApp'):
        base.__init__(self, name)
        return


    def main(self):
        self.inventory.reducer.getOutput( 'sqe' )
        return


    pass # end of PowderReductionApp


def main():
    app = PowderReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
