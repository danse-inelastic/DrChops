#include <cstring>
#include <iostream>

#include "histogram/EvenlySpacedGridData_4D.h"
#include "drchops/Histogrammer.h"


struct Event{
  unsigned int tof, pixelID;
};

struct Get
{
  void operator() 
  (const Event & e, 
   unsigned int & pack, unsigned int & tube, unsigned int &pixel, double &tof, 
   unsigned int &I) const 
  {
    pack = e.pixelID/1024 + 1;
    tube = e.pixelID/128 % 8;
    pixel = e.pixelID % 128;
    tof = e.tof/10.;
    I = 1;
  }
};


int main()
{
  
  using namespace DANSE::Histogram;
  using namespace DANSE::Reduction;
  
  typedef EvenlySpacedGridData_4D
    <unsigned int, unsigned int, unsigned int, double, unsigned int> 
    Ipdpt;
  
  unsigned int * intensities = new unsigned int[ 115*8*128*100 ];

  Ipdpt ipdpt
    ( 1, 116, 1, 
      0, 8, 1,
      0, 128, 1,
      1000, 2000, 10.,
      intensities );
  ipdpt.clear();
  assert (ipdpt(21, 3, 77, 1250) == 0);
  
  Get get;
  
  Histogrammer4
    <Event, Ipdpt, Get, 
    unsigned int, unsigned int, unsigned int,  double, 
    unsigned int> 
    her( ipdpt, get );
  
  Event e = { 12500, (21-1)*1024+3*128+77 };
  
  her( e );
  
  assert (ipdpt(21, 3, 77, 1250) == 1);

  delete [] intensities;
  return 0;
  
}

