## \package reduction.vectorCompat.fit_polynomial_QRFactorization
# fit data to a polynomial using QR factorization
#
# copied from mfit.py that was written by Max
# Here, we are solving a least squares problem using the QR Factorization:
# this can also be thought of as a column-wise Gram-Schmidt
# There is information on the row-wise version of this algorithm in:
#   _Matrix_Computation_ by Golub and Van Loan, on page 241
# linfit takes care of the linear case, and qfit the quadratic.  
# It's clear how to generalize to an N-degree polynomial. 
# (Just blindly follow the pattern)

def linfit(x,y):
  """ fit the given curve to a line
  y = a0 + a1 * x

  return a0, a1
  """
  import numpy as n
  from math import sqrt

  M = n.zeros( ( len(x), 2 ),'d' )
  M[:,0] = x
  M[:,1] = 1

  m,w = M.shape
  R = n.zeros((w,w),'d')
  Q = n.zeros((m,w),'d')

  v = M[:,0]
  R[0,0] = sqrt(n.add.reduce(v*v))
  Q[:,0] = v / R[0,0]

  for i in range(1,w):
    v = M[:,i]
    for j in range(0,i):
      p = Q[:,j]
      R[j,i] = n.add.reduce(v*p)
      v = v - R[j,i]*p
    R[i,i] = sqrt(n.add.reduce(v*v))
    Q[:,i] = v / R[i,i]

  w = len(R[0]);

#--This-is-here-because-the-matrixmultiply-algorithm-crashes-on-64-bits-------
  #Q = n.matrixmultiply( n.transpose(Q),y ) 
  tmp = n.zeros(len(n.transpose(Q)),'d')
  for i in range(len(tmp)):
    tmp[i] = n.add.reduce( (n.transpose(Q)[i])*y )
  Q = tmp
  del tmp
#-----------------------------------------------------------------------------
  result = n.zeros((w),'d');

  for i in range(w-1,-1,-1):
    for j in range(w-1,i-1,-1):
      Q[i] = Q[i] - R[i,j]*result[j]
    result[i] = Q[i]/R[i,i]
    continue

  result = list(result)
  result.reverse()
  
  return result


def qfit(x,y):
  """fit curve to a0+a1*x+a2*x^2

  return a0, a1, a2
  """
  import numpy as n
  from math import sqrt

  M = n.zeros( ( len(x), 3 ),'d' )
  M[:,0] = x*x
  M[:,1] = x
  M[:,2] = 1

  m,w = M.shape
  R = n.zeros((w,w),'d')
  Q = n.zeros((m,w),'d')

  v = M[:,0]
  R[0,0] = sqrt(n.add.reduce(v*v) )
  Q[:,0] = v / R[0,0]

  for i in range(1,w):
    v = M[:,i]
    for j in range(0,i):
      p = Q[:,j]
      R[j,i] = n.add.reduce(v*p)
      v = v - R[j,i]*p
    R[i,i] = sqrt(n.add.reduce(v*v))
    Q[:,i] = v / R[i,i]

  w = len(R[0]);

#--This-is-here-because-the-matrixmultiply-algorithm-crashes-on-64-bits-------
  #Q = n.matrixmultiply( n.transpose(Q),y ) 
  tmp = n.zeros(len(n.transpose(Q)),'d')
  for i in range(len(tmp)):
    tmp[i] = n.add.reduce( (n.transpose(Q)[i])*y )
  Q = tmp
  del tmp
#-----------------------------------------------------------------------------
  result = n.zeros((w),'d');

  for i in range(w-1,-1,-1):
    for j in range(w-1,i-1,-1):
      Q[i] = Q[i] - R[i,j]*result[j]
    result[i] = Q[i]/R[i,i]
    continue

  result = list(result)
  result.reverse()
    
  return result


