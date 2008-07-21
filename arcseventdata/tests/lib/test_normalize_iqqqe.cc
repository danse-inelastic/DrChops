#include <cstring>
#include <iostream>

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_iqqqe.h"
#include "arcseventdata/readPixelPositions.h"


int main()
{
  
  using namespace ARCS_EventData;

  double s[ 20 * 20 * 20 * 10 ];

  SaQQQE sa
    ( -10, 10, 1.,
      -10, 10, 1.,
      -10, 10, 1.,
      -50, 50, 10,
      s );

  double ei(70);
  NoMask mask;
  unsigned int npixels = 1024 * 100;
  double * pixelpositions = readPixelPositions( "pixelID2position.bin" );

  calcSolidAngleQQQE<SaQQQE, double, unsigned int>
    ( sa, ei, 
      0.025*1./128,
      npixels, pixelpositions, 
      mask);

  delete [] pixelpositions;
  
  return 0;
  
}

