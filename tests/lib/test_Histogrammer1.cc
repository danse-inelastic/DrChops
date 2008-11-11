#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_1D.h"
#include "drchops/Histogrammer.h"


struct Event{
  unsigned int tof;
};

struct Get
{
  void operator() ( const Event & e, unsigned int & tof, unsigned int & I ) const 
  {
    tof = e.tof;
    I = 1;
    return;
  }
};


int main()
{
  
  using namespace DANSE;
  using namespace DANSE::Histogram;
  using namespace DANSE::Reduction;
  
  typedef EvenlySpacedGridData_1D<unsigned int, unsigned int> Itof;
  
  unsigned int I[9];
  Itof itof( 1000, 10000, 1000, I );
  
  Get get;

  Histogrammer1<Event, Itof, Get, unsigned int, unsigned int> her( itof, get );

  
  Event e = { 3048 };
  
  her( e );
  
  assert (I[2] == 1);

  return 0;
  
}

