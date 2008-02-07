#include <iostream>
#include <fstream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2QE.h"

int main()
{

  using namespace ARCS_EventData;

  using namespace std;

  char *infilename = "pixelID2position.bin";
  ifstream is( infilename, ios::binary ); 
  if (! is.good() ) {
    std::cerr << "unable to open file" << infilename << std::endl;
    exit(1);
  }

  // get length of file:
  is.seekg (0, ios::end);
  int length; length = is.tellg();
  is.seekg (0, ios::beg);

  //check
  int npacks = 115, ndetsperpack = 8, npixelsperdet = 128, nbytesperdouble=8, ndoublepervector=3;
  assert(length==(npacks+1)*ndetsperpack*npixelsperdet*ndoublepervector*nbytesperdouble);

  // read
  char *buffer = new char[length];
  is.read( buffer, length );

  // 
  Event2QE event2qe( 70, (const double *)buffer );
  
  Event e = {60000, 2048};
  
  double Q,E;
  event2qe( e, Q,E );

  std::cout << "Q=" << Q << std::endl;
  std::cout << "E=" << E << std::endl;
  
  delete [] buffer;
  return 0;

}

