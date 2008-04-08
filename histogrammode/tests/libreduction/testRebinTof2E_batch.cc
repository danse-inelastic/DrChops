// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <cassert>
#include <cmath>
#include <iostream>
#include "reduction/RebinTof2E_batch.h"


void testIstartof2IE();
void testIstartof2IE_2();


int main()
{
  journal::debug_t debug( DANSE::Reduction::Universal1DRebinner_Impl::jrnltag );
  debug.activate();

  testIstartof2IE();
  testIstartof2IE_2();
}


#define NTOFBINS 100
#define NEBINS 30
#define NPIXELS 2


void testIstartof2IE_2()
{
  using namespace DANSE::Reduction;

  double distances[NPIXELS],  distance = 10000,
    tof[NTOFBINS+1], Ipixtof[(NTOFBINS)*NPIXELS], 
    e[NEBINS+1], IE[NEBINS], IEerr2[NEBINS],
    tmpe[NTOFBINS+1], tmpI[NEBINS];
  bool mask[NPIXELS];
  
  for (size_t i=0; i<NPIXELS; i++) {
    distances[i] = distance;
    mask[i] = 0;
  }

  // make tof axis, and I(tof) input histogram
  double tofmin = 3000., dtof = 100.;
  for (size_t i=0; i<NTOFBINS+1; i++) {
      tof[i] = tofmin + dtof * i;
  }
  
  // make I(pixel, tof). just one tof channel has counts
  size_t tofchannel = 30;
  for (size_t p=0; p<NPIXELS; p++) {
    for (size_t i=0; i<NTOFBINS; i++) {
      Ipixtof[i + p*(NTOFBINS)] = 0;
    }
    Ipixtof[tofchannel+p*NTOFBINS] = 1;
  }
  

  // make E axis and I(E) output histogram
  double e0 = tof2E( tof[0], distance ) * 1.2;
  double e1 = tof2E( tof[NTOFBINS], distance ) * 0.8;
  double de = (e0-e1)/NEBINS+1;

  // set I(E) to all zero
  std:: cout << "e axis: " << e0 << "," << e1 << std::endl;
  for (size_t i = 0; i<NEBINS+1; i++) {
    e[i] = e1 + de * i;
    std::cout << e[i] << ", ";
    if (i<NEBINS) IEerr2[i] = IE[i] = 0.0;
  }
  std::cout << std::endl;


  // rebinning
  Istartof2IE<double, double *, const double *, 
    double *, double *, const double *, const bool *>
    ( tof, tof+NTOFBINS+1, Ipixtof, Ipixtof, 
      e, e+NEBINS+1, IE, IEerr2, 
      distances, mask,
      NPIXELS,
      tmpe, tmpI);


  // now let us calculate the channel of E in which we should find counts
  double E = tof2E( tof[tofchannel], distance );
  size_t Echannel = int((E-e1)/de);
  std::cout << "expected E channel: " << Echannel << std::endl;
  // make sure I(E) is all zero except one channel
  std::cout << "I(E): " ;
  for (size_t i=0; i<NEBINS; i++) {
    std::cout << IE[i] << ", ";
  }
  std::cout << std::endl;
  for (size_t i=0; i<NEBINS; i++) {
    if (i==Echannel) assert(IE[i] == NPIXELS);
    else assert(IE[i] == 0);
  }
  return ;
}


void testIstartof2IE()
{
  using namespace DANSE::Reduction;
 
  double distance[NPIXELS], tof[10], Itof[9*NPIXELS], e[10], Ie[9], Ieerr2[9];
  double tmpe[10], tmpI[9];
  bool mask[NPIXELS] = {0,0};

  for (size_t i=0; i<10; i++) {
    tof[i] = 3000. + 100 * i;
  }

  for (size_t i=0; i<9*NPIXELS; i++) {
    Itof[i] = 1;
  }

  for (size_t i=0; i<NPIXELS; i++) {
    distance[i] = 10000;
  }

  for (size_t i=0; i<9; i++) {
    Ie[i] = 0; Ieerr2[i] = 0;
  }
  
  double e0 = tof2E( tof[0], distance[0] ) * 1.2;
  double e1 = tof2E( tof[9], distance[0] ) * 0.8;
  double de = (e0-e1)/10.;
  
  std:: cout << "e axis: " << e0 << "," << e1 << "," << de << std::endl;
  for (size_t i = 0; i<10; i++) {
    e[i] = e1 + de * i;
    std::cout << e[i] << ", ";
  }
  std::cout << std::endl;

  std::cout << "intensity: " << std::endl;
  for (size_t u=0; u<NPIXELS; u++) {
    for (size_t i=0; i<9; i++) {
      std::cout << Itof[u*9 + i] << ", ";
    }
    std::cout << std::endl;
  }
  std::cout << std::endl;

  Istartof2IE<double, double *, const double *, 
    double *, double *, const double *, const bool *>
    ( tof, tof+10, Itof, Itof, 
      e, e+10, Ie, Ieerr2, 
      distance, mask,
      NPIXELS,
      tmpe, tmpI);

  double sum = 0;
  std::cout << "I(E):" ;
  for (size_t i=0; i<9; i++) {
    std::cout << Ie[i] << ", ";
    sum += Ie[i];
  }
  std::cout << std::endl;

  double expected = 9*NPIXELS;
  assert ( (sum-expected)/expected < 1e-7 );
  return ;
}



// version
// $Id$

// End of file 
