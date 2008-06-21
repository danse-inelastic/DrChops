#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIxxxx.h"


using namespace ARCS_EventData;

//4D
class Event2pdpt: public Event2Quantity4<unsigned int, unsigned int, unsigned int, double>
{
  public:
  bool operator() ( const Event & e, 
		    unsigned int & pack, unsigned int & tube, unsigned int &pixel, double &tof ) const 
  {
    pack = e.pixelID/1024 + 1;
    tube = e.pixelID/128 % 8;
    pixel = e.pixelID % 128;
    tof = e.tof/10.;
    return 0;
  }
};


int main()
{  
  Event e = { 12500, (21-1)*1024+3*128+77 };

  Event2pdpt e2pdpt;

  size_t size = 115*8*128*100;
  unsigned int * intensities = new unsigned int[ size ];

  for (int i=0; i<size; i++) { intensities[i] = 0; }
  
  events2EvenlySpacedIxxxx<Event2pdpt, unsigned int, unsigned int, unsigned int, double, unsigned int>
    (&e, 1, e2pdpt, 
     1, 116, 1, 
     0, 8, 1,
     0, 128, 1,
     1000, 2000, 10.,
     intensities);

  assert (intensities[ ((21-1)*1024+3*128+77)*100 + 25] == 1);
  
  delete [] intensities;
  return 0;
}

