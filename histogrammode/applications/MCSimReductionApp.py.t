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


WEBSITE= "xxxWEBSITExxx"


from PowderReductionApp import PowderReductionApp as base

class MCSimReductionApp( base ):

    onelinehelp = "A handy tool for reducing simulated inelastic \n"\
                  "neutron scattering data.\n"
    gui_helpurl = "%s/click_monitor/MCSim_Reduction_GUI_Tutorial" % (
        WEBSITE, )
    helpurl ="%s/click_monitor/MCSim_Reduction" % (
        WEBSITE, )


    __doc__ = '''
MCSim Reduction Application
            
  Reduce simulated experiment data to S(Q,E).
            
  For more information, please read the online tutorial %s
  ''' % helpurl
    
    def __init__(self, name = "MCSimReductionApp" ):
        base.__init__(self, name )
        return

    pass # end of MCSimReductionApp

def main():
    import journal
    journal.error('pyre.inventory').deactivate()
    app = MCSimReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
