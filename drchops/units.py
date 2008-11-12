

from pyre.units import *
from pyre.units import unit, length, time, energy, pressure, angle

def isDimensional(d):
    return isinstance(d, unit.unit)

