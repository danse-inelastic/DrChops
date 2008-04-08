## \package reduction.pyre.PhiAxis
## provides pyre component to collect user input about phi axis.


from Axis import Axis

from reduction.pyre.inventory.Inventory import ObservableAdapter


class PhiAxis(Axis):

    """The 'phi' axis.

    This axis reperesents the scattering angle, i.e., the angle between
    the scattered beam and the incident neutron beam.
    
    An phi axis is defined by the minimum, the maximum, and the step size

    This pyre component is used to accept user inputs about a phi axis.
    """

    class Inventory(ObservableAdapter,Axis.Inventory):
        
        pass # end of Inventory


    def __init__(self, *args, **kwds):
        Axis.__init__(self, *args, **kwds)
        self.inventory.registerObserver( self )
        return


    def update(self, inventory):
        inv = inventory
        if inv.min-inv.step/2 <= 0:
            msg = "For 'phi' axis, all bin boundaries should be positive or zero. "\
                  "Please make sure min-step/2 > 0.\n" \
                  "Current inputs: min, step, boundary[0] = %s, %s, %s" % (
                inv.min, inv.step, inv.min-inv.step/2)
            raise ValueError , msg
        if inv.min >= inv.max-inv.step*2:
            msg = 'Invalid axis: min, step, max = ' % (inv.min, inv.step, inv.max)
            raise ValueError , msg
        return
        

    def _configure(self):
        Axis._configure(self)

        return


    pass # end of PhiAxis



