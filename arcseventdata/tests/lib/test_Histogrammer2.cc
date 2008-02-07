#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_2D.h"
#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/Histogrammer.h"


using namespace ARCS_EventData;

class Event2PixTofc: public Event2Quantity2<unsigned int, unsigned int>
{
  public:
  bool operator() ( const Event & e, unsigned int & pix, unsigned int & tof ) const 
  {
    pix = e.pixelID;
    tof = e.tof;
    return 0;
  }
};


int main()
{
  
  using namespace ARCS_EventData;
  using namespace DANSE::Histogram;
  
  typedef EvenlySpacedGridData_2D<unsigned int, unsigned int, unsigned int> Ipixtof;
  
  unsigned int intensities [100*9];
  Ipixtof ipixtof( 0, 100, 1, 1000, 10000, 1000, intensities );
  ipixtof.clear();
  assert (ipixtof(66, 3500) == 0);
  
  Event2PixTofc e2pt;
  
  Histogrammer2<Ipixtof, Event2PixTofc, unsigned int, unsigned int> her( ipixtof, e2pt );
  
  Event e = { 3500, 66 };
  
  her( e );
  
  assert (ipixtof(66, 3500) == 1);

  return 0;
  
}

