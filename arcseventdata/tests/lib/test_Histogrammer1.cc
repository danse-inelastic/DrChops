#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_1D.h"
#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/Histogrammer.h"


using namespace ARCS_EventData;

class Event2TofChannel: public Event2Quantity1<unsigned int>
{
  public:
  bool operator() ( const Event & e, unsigned int & tof ) const 
  {
    tof = e.tof;
    return 0;
  }
};


int main()
{
  
  using namespace ARCS_EventData;
  using namespace DANSE;
  
  typedef EvenlySpacedGridData_1D<unsigned int, unsigned int> Itof;
  
  unsigned int I[9];
  Itof itof( 1000, 10000, 1000, I );
  
  Event2TofChannel e2t;
  
  Histogrammer1<Itof, Event2TofChannel, unsigned int> her( itof, e2t );
  her.clear();
  
  Event e = { 3500, 2048 };
  
  her( e );
  
  assert (I[2] == 1);

  return 0;
  
}

