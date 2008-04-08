#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def minimizer( *args, **kwds ):
    """create a minimizer

    This minimizer uses differential evolution algorithm.

    Keywords:
      strategy = Best1Exp
      tolerance = 0.005
      termination = VTR(tolerance = 0.005)
      maxiter = ND*NP
      crossProbability = 1.0
      scalingFactor = 0.9
      stepMonitor = VerboseSow(30)
      sigintCallback = print_solution
    """
    tolerance = kwds.get('tolerance')
    if tolerance is not None:
        termination = VTR( tolerance )
        del kwds['tolerance']
        kwds['termination'] = termination
        pass
    return MinimizeFunction( *args, **kwds )

    



from mystic.differential_evolution import DifferentialEvolutionSolver2 as DifferentialEvolutionSolver
from mystic.detools import Best1Exp, Best1Bin, Rand1Exp, ChangeOverGeneration, VTR
from mystic import VerboseSow
import numpy


def print_solution( params, benchmark = None ):
    print params
    return



class MinimizeFunction:

    def __call__(self, f, box, NPoverND=None):
        if NPoverND is None: NPoverND = 30
        
        ND = len(box)
        NP = ND * NPoverND
        
        solver = DifferentialEvolutionSolver(ND, NP)

        boxT = numpy.array( box ).transpose()
        solver.SetRandomInitialPoints(min = boxT[0], max = boxT[1])

        solver.enable_signal_handler()

        maxiter = self.maxiter
        if maxiter is None: maxiter = _defaultMaxIter( ND, NP )
        
        solver.Solve(
            f, strategy = self.strategy, termination = self.termination,
            maxiter= maxiter,
            CrossProbability=self.crossProbability,
            ScalingFactor=self.scalingFactor,
            StepMonitor=self.stepMonitor,
            sigint_callback = self.sigintCallback,
            )

        solution = solver.Solution()
        return solution
    

    def __init__(
        self, strategy = Best1Exp, termination = VTR(0.005),
        maxiter = None, crossProbability = 0.9, scalingFactor = 0.78,
        stepMonitor = VerboseSow(30), sigintCallback = print_solution):

        self.strategy = strategy
        self.termination = termination
        self.maxiter = maxiter
        self.crossProbability = crossProbability
        self.scalingFactor = scalingFactor
        self.stepMonitor = stepMonitor
        self.sigintCallback = sigintCallback
        return

    pass # end of Minimize1DFunction



def _defaultMaxIter( ND, NP ): return ND * NP




def test():
    def f( X ):
        x,y = X
        return x*x + y*y

    minimizer = MinimizeFunction( )

    a,b = minimizer( f, [ (-1,1), (-1,1) ] )

    print a, b
    assert abs(a) < 0.1
    assert abs(b) < 0.1
    return


if __name__ == '__main__' : test()
    
    

# version
__id__ = "$Id$"

# End of file 
