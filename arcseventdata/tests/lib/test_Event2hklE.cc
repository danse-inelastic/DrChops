#include <iostream>
#include <fstream>
#include <cassert>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2hklE.h"

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
  assert(length==npacks*ndetsperpack*npixelsperdet*ndoublepervector*nbytesperdouble);

  // read
  char *buffer = new char[length];
  is.read( buffer, length );

  // ub
  double ub[9] = {1,0,0, 0,1,0, 0,0,1};
  Event2hklE event2hkle( 70, ub, (const double *)buffer );
  
  Event e = {60000, 2048};
  
  double h,k,l,E;
  event2hkle( e, h,k,l, E );

  std::cout << "hkl=" << h << "," << k << "," << l << std::endl;
  std::cout << "E=" << E << std::endl;
  
  delete [] buffer;
  return 0;

}

