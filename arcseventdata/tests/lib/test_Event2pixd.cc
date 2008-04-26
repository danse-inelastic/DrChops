#include <iostream>
#include <fstream>
#include <cassert>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2pixd.h"

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
  Event2pixd event2pixd( (const double *)buffer ) ;
  
  Event e = {30000, 2048};
  
  unsigned int pixelID;
  double d;
  event2pixd( e, pixelID, d );

  assert (pixelID==2048);
  std::cout << "d=" << d << std::endl;
  assert (d>0.1 && d<2);
  
  delete [] buffer;
  return 0;

}

