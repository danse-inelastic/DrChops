#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"


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
  return 0;
}

