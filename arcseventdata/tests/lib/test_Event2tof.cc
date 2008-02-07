#include <iostream>
#include <fstream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2tof.h"

int main()
{
  
  using namespace ARCS_EventData;
  using namespace std;
  
  Event2tof event2tof;
  
  Event e = {30000, 2048};
  
  double tof;
  event2tof( e, tof );
  
  assert (tof == 3.e-3 );
  
  return 0;

}

