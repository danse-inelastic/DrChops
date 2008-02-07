#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIxy.h"


using namespace ARCS_EventData;

class Event2PixTof: public Event2Quantity2<unsigned int, double>
{
  public:
  bool operator() ( const Event & e, unsigned int & pix, double & tof) const 
  {
    tof = e.tof * 0.1; // micro second
    pix = e.pixelID;
    return 0;
  }
};


int main()
{  
  Event e = { 3500, 2048 };

  Event2PixTof e2pt;

  unsigned int intensities[3*4];
  for (int i=0; i<3*4; i++) { intensities[i] = 0; }
  
  events2EvenlySpacedIxy<Event2PixTof, unsigned int, double, unsigned int>
    (&e, 1, e2pt, 0, 3000, 1000, 200, 600, 100, intensities);

  assert (intensities[9] == 1);
  
  return 0;
}

