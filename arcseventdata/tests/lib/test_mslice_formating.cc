#include <iostream>

#include "arcseventdata/mslice_formating.h"

int main()
{

  using namespace ARCS_EventData;

  size_t npixels = 10, nEbins = 16;

  size_t N = npixels*nEbins;

  double *S = new double[N], *Se = new double[N];

  for (size_t i=0; i<N; i++) {
    S[i] = Se[i] = i;
  }
  
  const char *s = SGrid_str( S, Se, npixels, nEbins );

  std::cout << s << std::endl;

  delete [] s;
  delete [] S;
  delete [] Se;
  return 0;

}

