#include <iostream>
#include <cassert>

#include "arcseventdata/pixel_solidangle.h"

int main()
{

  using namespace ARCS_EventData;

  double area = 1, x = 100., y = 0., z = 0.;
  double sa = pixel_solidangle<double> ( area, x, y, z ) ;
  assert (sa == 1.e-4);

  x = 400.; y = 0; z = 300.;
  sa = pixel_solidangle<double> ( area, x, y, z ) ;
  assert ( std::abs( sa / (1./500./500./500*400) - 1 ) < 1.e-3 );

  return 0;

}

