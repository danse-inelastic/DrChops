#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_2D.h"
#include "drchops/Histogrammer.h"


struct Event{
  unsigned int tof, pixelID;
};

struct Get
{
  public:
  void operator() 
  (const Event & e, unsigned int & pix, unsigned int & tof, unsigned int & I)
    const 
  {
    pix = e.pixelID;
    tof = e.tof;
    I = 1;
  }
};


int main()
{
  
  using namespace DANSE::Histogram;
  using namespace DANSE::Reduction;
  
  typedef EvenlySpacedGridData_2D<unsigned int, unsigned int, unsigned int> Ipixtof;
  
  unsigned int intensities [100*9];
  Ipixtof ipixtof( 0, 100, 1, 1000, 10000, 1000, intensities );

  assert (ipixtof(66, 3500) == 0);
  
  Get get;
  
  Histogrammer2<Event, Ipixtof, Get, unsigned int, unsigned int, unsigned int> 
    her( ipixtof, get );
  
  Event e = { 3500, 66 };
  
  her( e );
  
  assert (ipixtof(66, 3500) == 1);

  return 0;
  
}

