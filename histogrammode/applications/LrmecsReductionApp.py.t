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

class LrmecsReductionApp( base ):

    onelinehelp = "A handy tool for reducing inelastic neutron \n"\
                  "scattering data from LRMECS.\n"
    gui_helpurl = "%s/click_monitor/LRMECS_Reduction_GUI_Tutorial" % (
        WEBSITE, )
    helpurl ="%s/click_monitor/LRMECS_Reduction" % (
        WEBSITE, )


    __doc__ = '''
Lrmecs Reduction Application
            
  Reduce LRMECS experiment data to S(Q,E).
            
  For more information, please read the online tutorial %s
  ''' % helpurl
    
    def __init__(self, name = "LrmecsReductionApp" ):
        base.__init__(self, name )
        return

    pass # end of LrmecsReductionApp

def main():
    import journal
    journal.error('pyre.inventory').deactivate()
    app = LrmecsReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
