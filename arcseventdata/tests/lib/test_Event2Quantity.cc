#include <cstring>
#include <iostream>
#include <cassert>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"


using namespace ARCS_EventData;

class Event2TofChannel: public Event2Quantity1<unsigned int>
{
  public:
  unsigned int operator() ( const Event & e, unsigned int & d ) const 
  {
    d = e.tof;
    return 1;
  }
};


//4D
class Event2pdpt: public Event2Quantity4<unsigned int, unsigned int, unsigned int, double>
{
  public:
  unsigned int operator() ( const Event & e, 
		    unsigned int & pack, unsigned int & tube, unsigned int &pixel, double &tof ) const 
  {
    pack = e.pixelID/1024 + 1;
    tube = e.pixelID/128 % 8;
    pixel = e.pixelID % 128;
    tof = e.tof/10.;
    return 1;
  }
};


int test4d()
{
  Event2pdpt e2pdpt;
  
  Event event;
  event.tof = 1000; event.pixelID = 2048;

  unsigned int pack, tube, pixel;
  double tof;
  
  e2pdpt( event,  pack, tube, pixel, tof );
  
  assert (pack==3);
  assert (pixel == 0);
  assert (tube == 0);
  assert (tof == 100.);
}


int main()
{
  return 0;
}

