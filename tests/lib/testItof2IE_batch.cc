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
#include <vector>
#include "drchops/physics.h"
#include "drchops/Itof2IE_batch.h"


void test();
//void test2();


int main()
{
  journal::debug_t debug1(DANSE::Reduction::Universal1DRebinner_Impl::jrnltag);
  debug1.activate();

  journal::debug_t debug2(DANSE::Reduction::Itof2IE_batch_impl::jrnltag);
  debug2.activate();

  test();
  //test2();
}


#define NTOFBINS 1000
#define NPIXELS 10000
#define NEBINS 100


void test()
{
  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;

  double mod2sample=7000, distance = 3000;
  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  dblarr tofbb(NTOFBINS+1), Itof(NTOFBINS*NPIXELS), Ierr2_tof(NTOFBINS*NPIXELS),
    Ebb(NEBINS+1), IE(NEBINS*NPIXELS), Ierr2_E(NEBINS*NPIXELS),
    tmpEbb(NTOFBINS+1);

  double tofmin = 3000., dtof = 5;
  
  // I[pix, tof]
  std::cout << "preparing I[pix,tof]..." << std::endl;
  for (size_t i=0; i<NTOFBINS+1; i++) {
    tofbb[i] = tofmin + dtof * i;
    for (size_t p=0; p<NPIXELS; p++) 
      if (i<NTOFBINS) {
	size_t ind =i + p*NTOFBINS;
	Itof[ind] = Ierr2_tof[ind] = 1.;
      }
  }
  
  // incident energy
  double ei = 70;

  // tof from moderator to sample
  double tof0 = mod2sample/E2v(ei)*1000.;

  // find appropriate ef axis
  std::cout << "find appropriate ef axis..." << std::endl;
  double ef0 = tof2E( tofbb[0]-tof0, distance ) * 1.1;
  double ef1 = tof2E( tofbb[NTOFBINS]-tof0, distance ) * 0.9;
  double def = (ef0-ef1)/NEBINS;
  dblarr efbb(NEBINS+1);
  std:: cout << "ef axis: " << ef0 << "," << ef1 << std::endl;
  for (size_t i = 0; i<NEBINS+1; i++) {
    efbb[i] = ef0 - def * (i-0.5);
    std::cout << efbb[i] << ", ";
  }
  std::cout << std::endl;

  // convert ef to e
  dblarr ebb(NEBINS+1);
  std:: cout << "e axis: ";
  for (size_t i = 0; i< NEBINS+1; i++) {
    ebb[i] = ei - efbb[i];
    std::cout << ebb[i] << ", ";
  }
  std::cout << std::endl;

  // distance(pixel)
  dblarr dist( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) dist[i] = distance;

  std::cout << "Preparation of data finished. Start reduction..." << std::endl;

  Itof2IE_batch
    <double, dblIt, dblIt, dblIt, dblIt>
  ( tofbb.begin(), tofbb.end(),
    Itof.begin(), Ierr2_tof.begin(),
    
    ebb.begin(), ebb.end(),
    IE.begin(), Ierr2_E.begin(),

    ei, mod2sample,
    
    dist.begin(), 

    NPIXELS,
    
    tmpEbb.begin());

  std::cout << "testItof2IE_batch done." << std::endl;
  return ;
}



// version
// $Id$

// End of file 
