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
#include "reduction/physics.h"
#include "reduction/DGTS_RebinTof2E_batch.h"
#include "reduction/He3EfficiencyCorrection.h"


void test();
void test2();


int main()
{
  journal::debug_t debug( DANSE::Reduction::Universal1DRebinner_Impl::jrnltag );
  debug.activate();

  test();
  test2();
}


#define NTOFBINS 1000
#define NPIXELS 10000
#define NPHIBINS 100
#define NEBINS 100
#define NPIXELPERPHI 100


void test()
{
  // a test without detector efficiency correction
  // the pressure of detector is set to very high value so that detector efficiency
  // is always 1. 

  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;

  double mod2sample=7000, distance = 3000;
  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  dblarr tofbb(NTOFBINS+1), Itof(NTOFBINS*NPIXELS), 
    Ierr2_tof(NTOFBINS*NPIXELS),
    tmpEbb(NTOFBINS+1),
    tmpI(NEBINS); 

  double tofmin = 3000. , dtof = 5;
  
  // I[pix, tof]
  for (size_t i=0; i<NTOFBINS+1; i++) {
    tofbb[i] = tofmin + dtof * i;
    for (size_t p=0; p<NPIXELS; p++) 
      if (i<NTOFBINS) {
	size_t ind =i + p*NTOFBINS;
	Itof[ind] = Ierr2_tof[ind] = 1.;
      }
  }
  

  double ei = 70, tof0 = mod2sample/E2v(ei)*1000.;

  // find appropriate ef axis
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

  // phi axis
  dblarr phibb(NPHIBINS+1);
  for (size_t i=0; i< NPHIBINS+1; i++) phibb[i] = i;

  // S(phi,E)
  dblarr S(NPHIBINS* NEBINS), Serr2(NPHIBINS*NEBINS);
  for (size_t i=0; i< NPHIBINS*NEBINS; i++) {
    S[i] = 0; Serr2[i] = 0 ;
  }
  // solidangle output (phi)
  dblarr outsolidangle(NPHIBINS);
  for (size_t i=0; i< NPHIBINS; i++) {
    outsolidangle[i] = 0; 
  }

  // phi(pixel), solidangle(pixel)
  dblarr phi( NPIXELS ), solidangle( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) {phi[i] = i%100; solidangle[i] = 1.; }
  
  // distance(pixel)
  dblarr dist( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) dist[i] = distance;
  
  // radius(pixel), pressure(pixel)
  dblarr radius( NPIXELS ), pressure( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) {
    radius[i] = 1.27;
    pressure[i] = 100.; // so that efficiency is close to 1 and we can easily do comparison
  }
  
  // mask(pixel)
  boolarr mask( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) mask[i] = 0;

  std::cout << "Preparation of data finished. Start reduction..." << std::endl;

  DGTS_RebinTof2E_batch
    <double,
    dblIt, dblIt, dblIt, dblIt, boolIt,
    He3EfficiencyCorrection<double, std::vector<double>::iterator, dblIt >
    >
  ( tofbb.begin(), tofbb.end(),
    Itof.begin(), Ierr2_tof.begin(),
    
    phibb.begin(), phibb.end(),
    ebb.begin(), ebb.end(),
    S.begin(), Serr2.begin(), outsolidangle.begin(),
    
    ei, mod2sample,
    
    mask.begin(), phi.begin(), solidangle.begin(),
    dist.begin(), 
    radius.begin(), pressure.begin(),

    NPIXELS,
    
    tmpEbb.begin(), tmpI.begin() );

  /*
  std::cout << "reduced S(phi,E)" << std::endl; 
  for (size_t i=0; i<NPHIBINS; i++) {
    for (size_t j=0; j<NEBINS; j++) {
      std::cout << S[ i*NEBINS + j ] << ", ";
    }
    std::cout << std::endl;
  }
  */

  std::cout << "solidangle(phi)" << std::endl; 
  for (size_t i=0; i<NPHIBINS; i++) {
      std::cout << outsolidangle[ i ] << ", ";
    }
  
  std::cout << std::endl;

  // try to use jacobian to do rebin and compare to the results of rebinner
  //   1. we need deOverdtof
  double deOverdtof = def/dtof;
  double expected[NEBINS];
  for (size_t i=0; i<NEBINS; i++) {
    double efc = (efbb[i]+efbb[i+1])/2;
    double vf = sqrt( efc ) * 437.3949;
    double tof = distance/vf*1000.;
    expected[i] = tof/2./efc * deOverdtof;
    expected[i] *= NPIXELPERPHI;
  }

  // compare
  std::cout << "compare rebinned intensity to Expected:" << std::endl;
  for (size_t i=NEBINS/10; i<NEBINS*9/10; i++) {
    std::cout << S[i] << ", " << expected[i] << std::endl;
    assert( std::abs((S[i]-expected[i])/expected[i]) < 0.09 );
  }

  std::cout << "testDGTS_RebinTof2E_batch done." << std::endl;
  return ;
}


void test2()
{
  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;

  double mod2sample=7000, distance = 3000;
  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  dblarr tofbb(NTOFBINS+1), Itof(NTOFBINS*NPIXELS), 
    Ierr2_tof(NTOFBINS*NPIXELS),
    tmpEbb(NTOFBINS+1),
    tmpI(NEBINS); 

  double tofmin = 3000. , dtof = 5;
  
  // I[pix, tof]
  for (size_t i=0; i<NTOFBINS+1; i++) {
    tofbb[i] = tofmin + dtof * i;
    for (size_t p=0; p<NPIXELS; p++) 
      if (i<NTOFBINS) {
	size_t ind =i + p*NTOFBINS;
	Itof[ind] = Ierr2_tof[ind] = 1.;
      }
  }
  

  double ei = 70, tof0 = mod2sample/E2v(ei)*1000.;

  // find appropriate ef axis
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

  // phi axis
  dblarr phibb(NPHIBINS+1);
  for (size_t i=0; i< NPHIBINS+1; i++) phibb[i] = i;

  // S(phi,E)
  dblarr S(NPHIBINS* NEBINS), Serr2(NPHIBINS*NEBINS);
  for (size_t i=0; i< NPHIBINS*NEBINS; i++) {
    S[i] = 0; Serr2[i] = 0 ;
  }
  // solidangle output (phi)
  dblarr outsolidangle(NPHIBINS);
  for (size_t i=0; i< NPHIBINS; i++) {
    outsolidangle[i] = 0; 
  }

  // phi(pixel), solidangle(pixel)
  dblarr phi( NPIXELS ), solidangle( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) {phi[i] = i%100; solidangle[i] = 1.; }
  
  // distance(pixel)
  dblarr dist( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) dist[i] = distance;
  
  // radius(pixel), pressure(pixel)
  dblarr radius( NPIXELS ), pressure( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) {
    radius[i] = 1.27;
    pressure[i] = 10.; 
  }
  
  // mask(pixel)
  boolarr mask( NPIXELS );
  for (size_t i=0; i<NPIXELS; i++) mask[i] = 0;

  std::cout << "Preparation of data finished. Start reduction..." << std::endl;

  DGTS_RebinTof2E_batch
    <double,
    dblIt, dblIt, dblIt, dblIt, boolIt,
    He3EfficiencyCorrection<double, std::vector<double>::iterator, dblIt >
    >
  ( tofbb.begin(), tofbb.end(),
    Itof.begin(), Ierr2_tof.begin(),
    
    phibb.begin(), phibb.end(),
    ebb.begin(), ebb.end(),
    S.begin(), Serr2.begin(), outsolidangle.begin(),
    
    ei, mod2sample,
    
    mask.begin(), phi.begin(), solidangle.begin(),
    dist.begin(), 
    radius.begin(), pressure.begin(),

    NPIXELS,
    
    tmpEbb.begin(), tmpI.begin() );

  /*
  std::cout << "reduced S(phi,E)" << std::endl; 
  for (size_t i=0; i<NPHIBINS; i++) {
    for (size_t j=0; j<NEBINS; j++) {
      std::cout << S[ i*NEBINS + j ] << ", ";
    }
    std::cout << std::endl;
  }
  */
  std::cout << "solidangle(phi)" << std::endl; 
  for (size_t i=0; i<NPHIBINS; i++) {
      std::cout << outsolidangle[ i ] << ", ";
    }
  
  std::cout << std::endl;

  // try to use jacobian to do rebin and compare to the results of rebinner
  //   1. we need deOverdtof
  double deOverdtof = def/dtof;
  //   2. we need detector efficiency 
  dblarr efficiency(NEBINS), // efficiency
    efs(NEBINS); // Ef bin centers
  for (size_t i=0; i<NEBINS; i++) {
    efs[i] = (efbb[i]+efbb[i+1])/2;
  }
  He3DetEffic<double, dblIt> hde(pressure[0], radius[0], 200);
  hde( efs.begin(), efficiency.begin(), efficiency.end() );
  //   3. build the "expected" result
  double expected[NEBINS];
  for (size_t i=0; i<NEBINS; i++) {
    double efc = (efbb[i]+efbb[i+1])/2;
    double vf = sqrt( efc ) * 437.3949;
    double tof = distance/vf*1000.;
    expected[i] = tof/2./efc * deOverdtof; // jacobian
    expected[i] *= NPIXELPERPHI; // many pixels make their contributions. so we need this factor
    expected[i] /= efficiency[i]; // correct for detector efficiency
  }

  // compare
  std::cout << "compare rebinned intensity to Expected:" << std::endl;
  for (size_t i=NEBINS/10; i<NEBINS*9/10; i++) {
    std::cout << S[i] << ", " << expected[i] << std::endl;
    assert( std::abs((S[i]-expected[i])/expected[i]) < 0.09 );
  }

  std::cout << "testDGTS_RebinTof2E_batch done." << std::endl;
  return ;
}



// version
// $Id$

// End of file 
