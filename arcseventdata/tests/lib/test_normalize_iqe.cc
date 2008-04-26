#include <cstring>
#include <iostream>

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_iqe.h"
#include "arcseventdata/readPixelPositions.h"


int main()
{
  
  using namespace ARCS_EventData;

  double s[ 20 * 13 ];

  SaQE sa( 0, 13, 1., 
	   -50, 50, 5.,
	   s );

  double ei(70);
  NoMask mask;
  unsigned int npixels = 1024 * 100;
  double * pixelpositions = readPixelPositions( "pixelID2position.bin" );

  calcSolidAngleQE<SaQE, double, unsigned int>
    ( sa, ei, 
      npixels, pixelpositions, 
      mask);

  delete [] pixelpositions;
  
  return 0;
  
}

