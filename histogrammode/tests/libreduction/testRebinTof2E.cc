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
#include "reduction/RebinTof2E.h"


void test();
void test2();


int main()
{
  journal::debug_t debug( DANSE::Reduction::Universal1DRebinner_Impl::jrnltag );
  debug.activate();

  test();
  test2();
}


void test2()
{
  using namespace DANSE::Reduction;

#define NTOFCHANNELS 100
#define NECHANNELS 30


  double distance=10000, tof[NTOFCHANNELS],
    Itof[NTOFCHANNELS-1], e[NECHANNELS], Ie[NECHANNELS-1], tmpe[NTOFCHANNELS];
  
  // make tof axis, and I(tof) input histogram
  double tofmin = 3000., dtof = 100.;
  for (size_t i=0; i<NTOFCHANNELS; i++) {
    tof[i] = tofmin + dtof * i;
    if (i<NTOFCHANNELS-1) Itof[i] = 0.;
  }
  
  // just one tof channel has counts
  size_t tofchannel = 30;
  Itof[tofchannel] = 1;
  

  // make E axis and I(E) output histogram
  double e0 = tof2E( tof[0], distance ) * 1.2;
  double e1 = tof2E( tof[NTOFCHANNELS-1], distance ) * 0.8;
  double de = (e0-e1)/NECHANNELS;

  // set I(E) to all zero
  std:: cout << "e axis: " << e0 << "," << e1 << std::endl;
  for (size_t i = 0; i<NECHANNELS; i++) {
    e[i] = e1 + de * i;
    std::cout << e[i] << ", ";
    if (i<NECHANNELS-1) Ie[i] = 0.0;
  }
  std::cout << std::endl;

  // rebinner
  RebinTof2E<double, const double *, const double *, double *, double *>
    rebinner( distance );

  // rebinning
  rebinner( tof, tof+NTOFCHANNELS, Itof,
	    tmpe, 
	    e, e+NECHANNELS, Ie
	    );

  // now let us calculate the channel of E in which we should find counts
  double E = tof2E( tof[tofchannel], distance );
  size_t Echannel = int((E-e1)/de);
  std::cout << "expected E channel: " << Echannel << std::endl;
  // make sure I(E) is all zero except one channel
  std::cout << "I(E): " ;
  for (size_t i=0; i<NECHANNELS-1; i++) {
    std::cout << Ie[i] << ", ";
  }
  std::cout << std::endl;
  for (size_t i=0; i<NECHANNELS-1; i++) {
    if (i==Echannel) assert(Ie[i] == 1);
    else assert(Ie[i] == 0);
  }
  return ;
}


void test()
{
  using namespace DANSE::Reduction;

  double distance=10000, tof[10], Itof[9], e[10], Ie[9], tmpe[10];
  
  for (size_t i=0; i<10; i++) {
    tof[i] = 3000. + 100 * i;
    if (i<9) Itof[i] = 1.;
  }
  
  double e0 = tof2E( tof[0], distance ) * 1.1;
  double e1 = tof2E( tof[9], distance ) * 0.9;
  double de = (e0-e1)/10.;
  
  std:: cout << "e axis: " << e0 << "," << e1 << std::endl;
  for (size_t i = 0; i<10; i++) {
    e[i] = e1 + de * i;
    std::cout << e[i] << ", ";
    if (i<9) Ie[i] = 0.0;
  }
  std::cout << std::endl;

  RebinTof2E<double, const double *, const double *, double *, double *>
    rebinner( distance );

  rebinner( tof, tof+10, Itof,
	    tmpe, 
	    e, e+10, Ie
	    );

  double sum = 0;
  std::cout << "I(E): " ;
  for (size_t i=0; i<9; i++) {
    std::cout << Ie[i] << ", ";
    sum += Ie[i];
  }
  std::cout << std::endl;
  assert ( (sum-9)/9 < 1e-7 );
  return ;
}



// version
// $Id$

// End of file 
