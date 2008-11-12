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
#include "journal/debug.h"
#include "drchops/physics.h"
#include "drchops/IpixE2IphiE.h"


void test();


int main()
{
   journal::debug_t debug2(DANSE::Reduction::IpixE2IphiE_impl::jrnltag);
  debug2.activate();

  test();
  //test2();
}


#define NPIXELS 10000
#define NEBINS 120
#define NPHIBINS 115


void test()
{
  using namespace DANSE::Reduction;

  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  dblarr 
    Ebb(NEBINS+1), IpixE(NEBINS*NPIXELS), IE2pixE(NEBINS*NPIXELS);
  double Emin=-60, dE=1;

  // I[pix, E]
  std::cout << "preparing I[pix,E]..." << std::endl;
  for (size_t i=0; i<NEBINS+1; i++) {
    Ebb[i] = Emin + dE * i;
    for (size_t p=0; p<NPIXELS; p++) 
      if (i<NEBINS) {
	size_t ind = i + p*NEBINS;
	IpixE[ind] = IE2pixE[ind] = 1;
      }
  }

  // phi bins
  std::cout << "preparing phi bins..." << std::endl;
  dblarr
    phibb(NPHIBINS+1);
  double phimin=0, dphi=1, phimax = phimin + dphi*NPHIBINS;
  for (size_t i=0; i<NPHIBINS+1; i++) {
    phibb[i] = phimin + dphi * i;
  }
  
  // I[phi,E]
  std::cout << "preparing I[phi,E]..." << std::endl;
  dblarr IphiE(NPHIBINS*NEBINS), IE2phiE(NPHIBINS*NEBINS);
  // solidangle[phi]
  dblarr sa(NPHIBINS), saE2(NPHIBINS);
  
  // phi[pixel], solidangle[pixel], mask[pixel]
  dblarr phi(NPIXELS), solidangle(NPIXELS), solidangleE2(NPIXELS);
  boolarr mask(NPIXELS);
  std::cout << "preparing phi[pixel], solidangle[pixel], mask[pixel]..." << std::endl;
  for (size_t i=0; i<NPIXELS; i++) {
    phi[i] = i*phimax/NPIXELS;
    solidangle[i] = 1.; solidangleE2[i] = 0;
    mask[i] = 0;
  }

  std::cout << "Preparation of data finished. Start reduction..." << std::endl;

  IpixE2IphiE <double, dblIt, dblIt,dblIt, dblIt, boolIt>
    (Ebb.begin(), Ebb.end(),
     IpixE.begin(), IE2pixE.begin(),
     phibb.begin(), phibb.end(),
     IphiE.begin(), IE2phiE.begin(),
     sa.begin(), saE2.begin(),
      
     phi.begin(), solidangle.begin(), solidangleE2.begin(), mask.begin(),
     NPIXELS
     );
  
  std::cout << "testIpixE2IphiE_batch done." << std::endl;

  for (size_t i=0; i<NPHIBINS*NEBINS; i++) {
    assert (std::abs(IphiE[i] - NPIXELS/phimax) < 1 );
    //std::cout << IphiE[i] << ", ";
  }
  std::cout << std::endl;
  return ;
}



// version
// $Id$

// End of file 
