
def read( filename ):
    lines = open(filename).readlines()
    array = [  [ eval(t) for t in line.split() ] for line in lines ]
    import numpy
    return numpy.array(array).T

