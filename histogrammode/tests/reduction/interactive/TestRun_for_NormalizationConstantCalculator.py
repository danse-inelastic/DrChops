
from reduction import units
microsecond = units.time.microsecond
tofstep = 1 * microsecond


ic = 1000

class Run:

    def getMonitorItof(self, id):
        from histogram import histogram, arange
        itof = histogram(
            'I(tof)', [ ('tof', arange(3000,8000, tofstep/microsecond), 'microsecond') ] )
        itof.I[:] = id

        return itof


    def getIntegratedCurrent(self):
        return ic, None


    
