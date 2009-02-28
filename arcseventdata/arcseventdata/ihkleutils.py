
def tilt(IhklE, out_IhklE, tiltmatrix):
    from numpy.linalg import det
    from numpy import dot
    #create mapper
    def mapper(X):
        h,k,l,E = X
        h1,k1,l1 = dot(tiltmatrix, [h,k,l])
        return h1,k1,l1, E
    

    #the 'Jacobians'
    J = det(tiltmatrix)
    Jacobians = out_IhklE.copy()
    Jacobians.I[:] = J; Jacobians.E2[:] = 0
    
    #call rebinner
    from reduction.histCompat.Rebinner import rebinner
    rebinner.rebin(
        IhklE, out_IhklE,
        mapper,
        Jacobians, InversedJacobains = False,
        epsilon = -1)
    
    return

