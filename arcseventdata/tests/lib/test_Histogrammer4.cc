#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_4D.h"
#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/Histogrammer.h"


using namespace ARCS_EventData;

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


int main()
{
  
  using namespace ARCS_EventData;
  using namespace DANSE::Histogram;
  
  typedef EvenlySpacedGridData_4D<unsigned int, unsigned int, unsigned int, double, unsigned int> Ipdpt;
  
  unsigned int * intensities = new unsigned int[ 115*8*128*100 ];

  Ipdpt ipdpt
    ( 1, 116, 1, 
      0, 8, 1,
      0, 128, 1,
      1000, 2000, 10.,
      intensities );
  ipdpt.clear();
  assert (ipdpt(21, 3, 77, 1250) == 0);
  
  Event2pdpt e2pdpt;
  
  Histogrammer4<Event, Ipdpt, Event2pdpt, unsigned int, unsigned int, unsigned int,  double, unsigned int> 
    her( ipdpt, e2pdpt );
  
  Event e = { 12500, (21-1)*1024+3*128+77 };
  
  her( e );
  
  assert (ipdpt(21, 3, 77, 1250) == 1);

  delete [] intensities;
  return 0;
  
}

