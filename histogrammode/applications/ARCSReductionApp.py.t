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


WEBSERVER= "xxxWEBSERVERxxx"


from PowderReductionApp import PowderReductionApp as base

class ARCSReductionApp( base ):

    onelinehelp = "A handy tool for reducing ARCS inelastic \n"\
                  "neutron scattering data.\n"
    gui_helpurl = "%s/click_monitor/ARCS_Reduction_GUI_Tutorial" % (
        WEBSERVER, )
    helpurl ="%s/click_monitor/ARCS_Reduction" % (
        WEBSERVER, )


    __doc__ = '''
ARCS Reduction Application
            
  Reduce simulated experiment data to S(Q,E).
  
  For more information, please read the online tutorial %s
  ''' % helpurl
    
    def __init__(self, name = "ARCSReductionApp" ):
        base.__init__(self, name )
        return

    pass # end of ARCSReductionApp

def main():
    import journal
    journal.error('pyre.inventory').deactivate()
    app = ARCSReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
