#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/IxHistogrammer.h"


using namespace ARCS_EventData;
using namespace DANSE;

class Event2TofChannel: public Event2Quantity1<unsigned int>
{
  public:
  bool operator() ( const Event & e, unsigned int & d ) const 
  {
    d = e.tof;
    return 0;
  }
};


int main()
{  
  Event2TofChannel e2t;
  IxHistogrammer< unsigned int, Event2TofChannel, unsigned int > her( 1000, 8000, 1000, e2t );
  her.clear();
  
  Event e = { 3500, 2048 };
  
  her( e );

  assert (her.Iarray()[2] == 1);

  delete [] her.Iarray();

  return 0;
}

