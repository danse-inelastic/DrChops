#include <cstring>
#include <iostream>
#include <fstream>

#include "drchops/solidangle_qe.h"
#include "drchops/readPixelPositions.h"


double * readSolidAngles(const char *fn, int npixels)
{
  double * ret = new double [npixels];
  std::ifstream ifs(fn, std::ios::binary);
  ifs.read( (char *)ret, npixels * sizeof(double));
  return ret;
}


int main()
{
  
  USING_DRCHOPS_NAMESPACE;

  double s[ 20 * 13 ];

  SaQE sa( 0, 13, 1., 
	   -50, 50, 5.,
	   s );

  double ei(70);
  unsigned int npixels = 1024 * 100;
  double * pixelpositions = readPixelPositions( "pixelID2position.bin" );
  double * solidangles = readSolidAngles("solidangles.bin", npixels);
  
  calcSolidAngleQE<SaQE, double, unsigned int>
    ( sa, ei, 
      npixels, pixelpositions, solidangles
      );

  delete [] pixelpositions;
  delete [] solidangles;
  
  return 0;
  
}

