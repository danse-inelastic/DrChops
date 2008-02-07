#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIx.h"


using namespace ARCS_EventData;

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
  Event e = { 3500, 2048 };

  Event2TofChannel e2t;

  unsigned int intensities[7];
  for (int i=0; i<7; i++) { intensities[i] = 0; }
  
  events2EvenlySpacedIx<Event2TofChannel, unsigned int, unsigned int>
    (&e, 1, e2t, 1000, 8000, 1000, intensities);

  assert (intensities[2] == 1);
  
  return 0;
}

