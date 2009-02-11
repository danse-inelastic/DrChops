#include <cstring>
#include <iostream>

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_ihkle.h"
#include "arcseventdata/readPixelPositions.h"


int main()
{
  
  using namespace ARCS_EventData;

  double s[ 20 * 20 * 20 * 10 ];

  SaHKLE sa
    ( -10, 10, 1.,
      -10, 10, 1.,
      -10, 10, 1.,
      -50, 50, 10,
      s );

  double ei(70);
  double ub_store[9] = {1,0,0, 0,1,0, 0,0,1};
  double *ub[3];
  for (int i=0; i<3; i++) {
    ub[i] = ub_store+i*3;
  }

  NoMask mask;
  unsigned int npixels = 1024 * 100;
  double * pixelpositions = readPixelPositions( "pixelID2position.bin" );

  calcSolidAngleHKLE<SaHKLE, double, unsigned int>
    ( sa, ei, ub,
      0.025*1./128,
      npixels, pixelpositions, 
      mask);

  delete [] pixelpositions;
  
  return 0;
  
}

