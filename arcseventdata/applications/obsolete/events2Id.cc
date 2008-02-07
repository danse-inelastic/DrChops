#include <cstring>
#include <iostream>
#include <fstream>

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2d.h"
#include "arcseventdata/events2Ix.h"
#include "arcseventdata/Idspacing.h"
#include "arcseventdata/EventsReader.h"
#include "arcseventdata/ioutils.h"


/// convert event data file to I(d) histogram
/// d-spacing

double *readPixelPositions( const char * infilename )
{
  using namespace std;
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
  is.close();

  return (double *) buffer;
}


int run( const char *eventfilename,  size_t Nevents, 
	 const char *pixelPositionsFilename, 
	 double dbegin, double dend, double dstep,
	 const char *outfilename)
{
  using namespace ARCS_EventData;

  // read events
  EventsReader reader( eventfilename );

  Event * pevents = reader.read( Nevents );

  unsigned int * intensities = new unsigned int [size_t((dend-dbegin)/dstep)];
  Idspacing i_d( dbegin, dend, dstep, intensities );

  i_d.clear();

  double *pixelPositions = readPixelPositions( pixelPositionsFilename );
  Event2d e2d( pixelPositions );
  events2Ix< Event2d, Idspacing > (pevents, Nevents, e2d, i_d);

  delete [] pevents;

  // save histogram to a 2col ascii
  dumpIx<double, unsigned int>( i_d, outfilename );

  delete [] pixelPositions;
  delete [] intensities;

  return 0;
}

void help()
{
  std::cout << "idspacing event-data-filename Nevents pixel-positions-filename dbegin dend dstep output-filename" << std::endl;
  std::cout << " * units: " << std::endl
	    << "   d: 1 Angstrom" << std::endl;
}


int main( int argc, char ** argv )
{
  if (argc != 8 ) { help(); exit(1); }

  char *eventfilename = argv[1];

  size_t Nevents = atoi( argv[2] );

  char *pixelPositionsFilename = argv[3];
  
  double dbegin = atof( argv[4] );
  double dend = atof( argv[5] );
  double dstep = atof( argv[6] );

  char *ofilename = argv[7];

  run( eventfilename, Nevents, pixelPositionsFilename, dbegin, dend, dstep, ofilename );

  return 0;
}



