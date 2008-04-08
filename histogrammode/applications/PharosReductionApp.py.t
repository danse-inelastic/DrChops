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

class PharosReductionApp( base ):

    onelinehelp = "A handy tool for reducing inelastic neutron \n"\
                  "scattering data from PHAROS.\n"
    gui_helpurl = "%s/click_monitor/PHAROS_Reduction_GUI_Tutorial" % (
        WEBSITE, )
    helpurl ="%s/click_monitor/PHAROS_Reduction" % (
        WEBSITE, )


    __doc__ = '''
Pharos Reduction Application
            
  Reduce PHAROS experiment data to S(Q,E).
            
  For more information, please read the online tutorial %s
  ''' % helpurl
    
    class Inventory(base.Inventory):
        pass

    def __init__(self, name = "PharosReductionApp" ):
        base.__init__(self, name )
        return

    pass # end of PharosReductionApp

def main():
    import journal
    journal.error('pyre.inventory').deactivate()
    journal.warning('PharosDetCSVParser').deactivate()
    app = PharosReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
