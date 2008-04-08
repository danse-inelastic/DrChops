## \package reduction.pyre.Axis
## provides pyre component to collect user input about an axis.


from pyre.components.Component import Component

class Axis(Component):

    """An axis is used to describe a sequence of values for a physical
    quantity.

    An axis is defined by the minimum, the maximum, and the step size
    """

    class Inventory(Component.Inventory):
        import pyre.inventory as inv

        min = inv.float("min", default = 0.0 )
        min.meta['tip'] = "Minimum"
        min.meta['importance'] = 1000
        
        max = inv.float("max", default = 10.0 )
        max.meta['tip'] = "Maximum"
        max.meta['importance'] = 900

        step = inv.float("step", default = 1.0 )
        step.meta['tip'] = "Step"
        step.meta['importance'] = 800

        unit = inv.str('unit', default = '1')
        unit.meta['tip'] = 'unit'
        unit.meta['importance'] = 700
        unit.meta['opacity'] = 100

        pass # end of Inventory


    def __init__(self, name,
                 min = 0., max = 10., step = 1., unit = '1',
                 dummy = False, facility = 'Axis',
                 ):
        Component.__init__(self, name, facility)
        self._dummy = dummy
        si = self.inventory
        si.min = min; si.max = max; si.step = step; si.unit = unit
        return


    def __call__(self):
        if self._dummy: return None
        from histogram import axis, arange
        name = self.name
        return axis( name, arange(self.min, self.max, self.step),
                     unit = self.unit)


    def _configure(self):
        Component._configure(self)
        si = self.inventory
        self.min = si.min; self.max = si.max; self.step = si.step
        self.unit = si.unit
        return


    pass # end of Axis



