#include "arcseventdata/littleEndian2bigEndian.h"
#include <iostream>
#include <fstream>


using namespace std;

int run( char * infilename, char * outfilename )
{
  // open input
  ifstream is( infilename, ios_base::binary );

  if ( is.bad() )
    std::cerr << "unable to open file" << infilename << std::endl;

  // get length of file:
  is.seekg (0, ios::end);
  int length; length = is.tellg();
  is.seekg (0, ios::beg);

  assert (length % 4==0); // make sure it is an int array

  // read data
  char *buffer = new char[length];
  is.read( buffer, length);
  is.close();

  // to convert, we need int pointer
  int *b = (int *) buffer;
  // new array to hold results
  int *ret = new int[ length/4 ];

  // convert
  for (int i=0; i<length/4; i++) 
    ret[i] = INT_little_endian_TO_big_endian(b[i]);

  // write results to output file
  ofstream os( outfilename, ios::binary );
  os.write( (char *)ret, length );
  os.close();
 
  delete [] buffer;
  delete [] ret;
  return 0;
}

void help()
{
  std::cout << "l2b eventdatafile_littleendian eventdatafile_bigendian" << std::endl;
}

int main( int argc, char **argv )
{

  if (argc != 3) { help(); exit(2); }
  
  char *in = argv[1];
  char *out = argv[2];

  run( in, out );

}

