#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


try:
    import mpi
    from arcseventdata.pyre_support.MpiApplication import Application as base
except ImportError:
    import journal
    import traceback
    journal.warning('mpi').log('mpi not available: %s' % traceback.format_exc())
    from pyre.applications.Script import Script as base


class ArcsreducevanadiumdataApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        vrun = pyre.inventory.str('vrun', default='ARCS_297')
        vrun.meta['tip'] = 'The vanadium run data directory'

        ARCSxml = pyre.inventory.str('x', default='ARCS.xml')
        ARCSxml.meta['tip'] = 'The instrument xml file for ARCS'

        from reduction.pyre.inventory.properties.NumberList import NumberList
        E_params = NumberList('E_params', default=(-60,60,1.))
        E_params.meta['tip'] = 'Define Energy axis: min, max, step'

        Ei = pyre.inventory.float('Ei', default=99)
        Ei.meta['tip'] = 'Nominal incident neutron energy for this vanadium calibration run'

        mask_counts_bracket = NumberList('m', default=(10,0))
        mask_counts_bracket.meta['tip'] = "lowerlimist,upperlimit for mask generation"
        
        calibration_output = pyre.inventory.str('calibration-output', default = 'calibration.h5')
        calibration_output.meta['tip'] = 'output file name for calibration constants'

        mask_output = pyre.inventory.str('mask-output', default = 'mask.h5')
        mask_output.meta['tip'] = 'output file name for mask'


    def main(self, *args, **kwds):
        vrun = self.vrun
        ARCSxml = self.ARCSxml
        E_params = self.E_params
        Ei = self.Ei
        lowerlimit, upperlimit = self.mask_counts_bracket
        from reduction.core.ARCS.ReduceVanadiumData import reduce
        reduced = reduce(
            vrun, ARCSxml = ARCSxml,
            E_params = E_params, Ei = Ei,
            criteria_nocounts = lowerlimit,
            criteria_toomanycounts = upperlimit)
        
        calibration = reduced['calibration']
        mask = reduced['mask']

        calibration_output = self.inventory.calibration_output
        mask_output = self.mask_output
        from histogram.hdf import dump
        dump( calibration, calibration_output, '/', 'c' )
        dump( mask, mask_output, '/', 'c' )
        return


    def __init__(self):
        base.__init__(self, 'ARCSReduceVanadiumData')
        return


    def _configure(self):
        base._configure(self)
        self.vrun = self.inventory.vrun
        self.ARCSxml = self.inventory.ARCSxml
        self.E_params = self.inventory.E_params
        self.Ei = self.inventory.Ei
        lowerlimit, upperlimit = self.inventory.mask_counts_bracket
        if lowerlimit == 0: lowerlimit = None
        if upperlimit == 0: upperlimit = None
        self.mask_counts_bracket = lowerlimit, upperlimit

        self.calibration_output = self.inventory.calibration_output
        self.mask_output = self.inventory.mask_output
        return


    def _init(self):
        base._init(self)
        calibration_output = self.inventory.calibration_output
        mask_output = self.mask_output
        outputs = [ calibration_output, mask_output ]
        for o in outputs: self._check_output_file(o)
        return


    def _check_output_file(self, f):
        import os
        if os.path.exists( f ):
            raise RuntimeError, "Output file %r already exists" % f
        return


def main():
    app = ArcsreducevanadiumdataApp()
    import os
    print "times: %s" % str(os.times())
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
