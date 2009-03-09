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


class ARCSReduceToMsliceFilesApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        mainrun = pyre.inventory.str('r', default='') #'ARCS_279')
        mainrun.meta['tip'] = 'The main run data directory'

        mtrun = pyre.inventory.str('M', default='') #'ARCS_289'
        mtrun.meta['tip'] = 'The emtpy can run data directory'

        mtratio = pyre.inventory.float('R', default=0.9)
        mtratio.meta['tip'] = 'multiplier for empty can run'

        ARCSxml = pyre.inventory.str('x', default='ARCS.xml')
        ARCSxml.meta['tip'] = 'The instrument xml file for ARCS'

        from reduction.pyre.inventory.properties.NumberList import NumberList
        E_params = NumberList('E', default=(-60,60,1.))
        E_params.meta['tip'] = 'Define Energy axis: min, max, step'

        tof_params = NumberList('t', default=(3000,6000,5.))
        tof_params.meta['tip'] = 'Define tof axis: min, max, step'

        pack_params = NumberList('pack', default=(1,115))
        pixel_resolution = pyre.inventory.int('pixel-resolution', default=1)

        Ei = pyre.inventory.float('I', default=99)
        Ei.meta['tip'] = 'Nominal incident neutron energy for this vanadium calibration run'

        #mask_counts_bracket = NumberList('m', default=(10,0))
        #mask_counts_bracket.meta['tip'] = "lowerlimist,upperlimit for mask generation"
        
        calibration = pyre.inventory.str('calibration', default = 'calibration.h5')
        calibration.meta['tip'] = 'file path for calibration constants'

        mask = pyre.inventory.str('mask', default = 'mask.h5')
        mask.meta['tip'] = 'file path for mask'

        outputprefix = pyre.inventory.str('outputprefix', default = 'mslice' )


    def main(self, *args, **kwds):
        mainrun = self.mainrun
        mtrun = self.mtrun
        mtratio = self.mtratio
        ARCSxml = self.ARCSxml
        E_params = self.E_params
        tof_params = self.tof_params
        pack_params = self.pack_params
        pixel_resolution = self.pixel_resolution
        Ei = self.Ei
        #lowerlimit, upperlimit = self.mask_counts_bracket
        calibration = self.calibration
        mask = self.mask
        outputprefix = self.outputprefix
        from reduction.core.ARCS.ReduceToMslice import reduce
        sqe = reduce(
            mainrun,
            mtrundir = mtrun, mtratio = mtratio,
            #criteria_nocounts = lowerlimit,
            #criteria_toomanycounts = upperlimit,
            calibration = calibration, mask = mask,
            ARCSxml = ARCSxml,
            tof_params = tof_params,
            E_params = E_params,
            Ei = Ei,
            outputprefix = outputprefix,
            pack_params = pack_params,
            pixel_resolution = pixel_resolution,
            )
        return


    def __init__(self):
        base.__init__(self, 'ARCSReduceToMsliceFiles')
        return


    def _configure(self):
        base._configure(self)
        self.mainrun = self.inventory.mainrun
        
        mtrun = self.inventory.mtrun
        if mtrun == '': mtrun = None
        self.mtrun = mtrun

        self.mtratio = self.inventory.mtratio
        self.ARCSxml = self.inventory.ARCSxml
        self.E_params = self.inventory.E_params
        self.tof_params = self.inventory.tof_params
        self.pack_params = self.inventory.pack_params
        self.pixel_resolution = self.inventory.pixel_resolution
        self.Ei = self.inventory.Ei
        #lowerlimit, upperlimit = self.inventory.mask_counts_bracket
        #if lowerlimit == 0: lowerlimit = None
        #if upperlimit == 0: upperlimit = None
        #self.mask_counts_bracket = lowerlimit, upperlimit

        self.calibration = self.inventory.calibration
        self.mask = self.inventory.mask
        
        self.outputprefix = self.inventory.outputprefix
        return


    def _init(self):
        base._init(self)
        if self._showHelpOnly: return
        calibration = self.calibration
        mask = self.mask
        inputs = [ calibration, mask ]
        for i in inputs: self._check_input_file(i)
        import histogram.hdf as hh
        self.mask = hh.load( mask, 'mask' )
        self.calibration = hh.load( calibration, 'calibration' )

        from reduction.core.ARCS.ReduceToMslice import mslice_output_filenames
        prefix = self.outputprefix
        outputs = mslice_output_filenames(prefix)
        for o in outputs: self._check_output_file(o)
        return


    def _check_output_file(self, f):
        import os
        if os.path.exists( f ):
            raise RuntimeError, "Output file %r already exists" % f
        return


    def _check_input_file(self, f):
        import os
        if not os.path.exists( f ):
            raise RuntimeError, "Input file %r does not exist" % f
        return


def main():
    app = ARCSReduceToMsliceFilesApp()
    import os
    app.run()
    print "times: %s" % str(os.times())
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
