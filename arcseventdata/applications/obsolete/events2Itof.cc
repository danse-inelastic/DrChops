#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/events2Ix.h"
#include "arcseventdata/Itof.h"
#include "arcseventdata/EventsReader.h"
#include "arcseventdata/ioutils.h"


int run( const char *filename,  size_t Nevents, 
	 unsigned int tofbegin, unsigned int tofend, unsigned int tofstep,
	 const char *outfilename)
{

  using namespace ARCS_EventData;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  // make the histogram
  Itofchannel itof( tofbegin, tofend, tofstep );
  itof.clear();
  
  // histogramming...
  events2Ix< Event2TofChannel, Itofchannel > (pevents, Nevents, e2tc, itof);

  // no longer need events
  delete [] pevents;

  // save histogram to a 2col ascii
  dumpIx<unsigned int, unsigned int>( itof, outfilename );

  // clean up
  unsigned int * intensities = itof.intensities;
  delete [] intensities;

  return 0;
}

void help()
{
  std::cout << "itof event-data-filename Nevents tofbegin tofend tofstep output-filename" << std::endl;
  std::cout << " * units: " << std::endl
	    << "   tof: 100us" << std::endl;
}


int main( int argc, char ** argv )
{
  if (argc != 7 ) { help(); exit(1); }

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int tofbegin = atoi( argv[3] );
  unsigned int tofend = atoi( argv[4] );
  unsigned int tofstep = atoi( argv[5] );

  char *ofilename = argv[6];

  run( filename, Nevents, tofbegin, tofend, tofstep, ofilename );

  return 0;
}



