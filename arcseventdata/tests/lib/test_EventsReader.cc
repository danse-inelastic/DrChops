#include <iostream>
#include <fstream>

#include "arcseventdata/EventsReader.h"

void test1()
{

  using namespace ARCS_EventData;

  EventsReader reader( "events.dat" );

  size_t N = 10;

  Event * pevents = reader.read( N );

  for (int i=0; i<N; i++) {
    std::cout << pevents[i].tof << ", " << pevents[i].pixelID << std::endl ;
  }

  delete [] pevents;

  return;
}


void test2()
{

  using namespace ARCS_EventData;

  EventsReader reader( "events.dat" );

  size_t n1 = 10, n2 = 20, N=n2-n1;

  Event * pevents = reader.read( n1, n2 );

  for (int i=0; i<N; i++) {
    std::cout << pevents[i].tof << ", " << pevents[i].pixelID << std::endl ;
  }

  delete [] pevents;

  return;
}


void test2a()
{

  using namespace ARCS_EventData;

  EventsReader reader( "events.dat" );

  size_t n1 = 0, n2 = 10, N=n2-n1;

  Event * pevents = reader.read( n1, n2 );

  for (int i=0; i<N; i++) {
    std::cout << pevents[i].tof << ", " << pevents[i].pixelID << std::endl ;
  }

  delete [] pevents;

  return;
}


int main()
{
  test1();
  test2();
  test2a();
}
