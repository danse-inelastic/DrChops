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
#include "reduction/physics.h"
#include "reduction/DGTS_RebinTof2E.h"


void test();
void test2();
void test_DTGS_Tof2EFunctor();


int main()
{
  journal::debug_t debug( DANSE::Reduction::Universal1DRebinner_Impl::jrnltag );
  debug.activate();

  test();
  test2();
  test_DTGS_Tof2EFunctor();
}



template <typename Iterator>
void printVector( char * name,  const Iterator begin, const Iterator end )
{
  Iterator it = begin;
  std::cout << name;
  for ( ; it < end; it++ )
    std::cout << *it << ", ";
  std::cout << std::endl;
}


void test_DTGS_Tof2EFunctor()
{
  double ei(60.), mod2sample(8123.7), tof(3150.), sample2det = 2500.;
  
  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;
  
  double vi = E2v(ei);
  std::cout << "ei = " << ei << ", vi = " << vi << std::endl;
  double tof0 = mod2sample/E2v( ei ) * 1000.;

  double tof1 = tof - tof0;
  
  double ef = v2E( sample2det/tof1 * 1000. );
  
  double e = ei - ef;

  DGTS_Tof2EFunctor<double>  f( ei, mod2sample, sample2det );
  std::cout << "e = " << e << std::endl;
  assert (e == f(tof));
  assert (e < 3. && e > -3.);
  std::cout << "test_DTGS_Tof2EFunctor done." << std::endl;
}


void test()
{
  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;

  double mod2sample=7000, distance = 3000, \
    tof[10], Itof[9], ef[10], Ie[9], tmpe[10];
  
  for (size_t i=0; i<10; i++) {
    tof[i] = 3000. + 100 * i;
    if (i<9) Itof[i] = 1.;
  }
  
  double ei = 70, tof0 = mod2sample/E2v(ei)*1000.;

  double ef0 = tof2E( tof[0]-tof0, distance ) * 1.1;
  double ef1 = tof2E( tof[9]-tof0, distance ) * 0.9;
  double def = (ef0-ef1)/10.;
  std:: cout << "ef axis: " << ef0 << "," << ef1 << std::endl;
  for (size_t i = 0; i<10; i++) {
    ef[i] = ef0 - def * i;
    std::cout << ef[i] << ", ";
    if (i<9) Ie[i] = 0.0;
  }
  std::cout << std::endl;

  double e[10];
  std:: cout << "e axis: ";
  for (size_t i = 0; i< 10; i++) {
    e[i] = ei - ef[i];
    std::cout << e[i] << ", ";
  }
  std::cout << std::endl;

  DGTS_RebinTof2E<double, const double *, const double *,
    double *, double *> \
    rebinner( ei, mod2sample );

  rebinner.set_distance( distance );

  rebinner( tof, tof+10, Itof,
	    tmpe, 
	    e, e+10, Ie
	    );

  std::cout << "rebinned intensity: ";
  double sum = 0;
  for (size_t i=0; i<9; i++) {
    std::cout << Ie[i] << ", ";
    sum += Ie[i];
  }
  std::cout << std::endl;

  assert ( (sum-9)/9 < 1e-7 );

  std::cout << "test passed" << std::endl;
  return ;
}


void test2()
{
  using namespace DANSE::Reduction;
  using namespace DANSE::Physics::Units::Conversion;

  size_t NTOFBBS=101, NTOFBINS=NTOFBBS-1, NEBINS=NTOFBINS/5, NEBBS= NEBINS+1;

  double ei = 70;

  double mod2sample=7000, distance = 3000, \
    tof[NTOFBBS], Itof[NTOFBINS], ef[NEBINS+1], Ie[NEBINS], tmpe[NTOFBBS];
  
  double  tofmin = 1000.*mod2sample/E2v(ei), tofmax = tofmin+4000, 
    dtof = (tofmax-tofmin)/NTOFBBS;
  for (size_t i=0; i<NTOFBBS; i++) {
    tof[i] = tofmin + dtof * i;
    if (i<NTOFBINS) Itof[i] = 1.;
  }
  
  double ef0 = 110;
  double ef1 = 30;
  double def = (ef0-ef1)/NEBINS;
  std:: cout << "ef axis: " << "ef0=" << ef0 << "," << "ef1=" << ef1 << std::endl;
  for (size_t i = 0; i<NEBBS; i++) {
    ef[i] = ef0 - def * i;
    std::cout << ef[i] << ", ";
    if (i<NEBINS) Ie[i] = 0.0;
  }
  std::cout << std::endl;

  double e[NEBBS];
  std:: cout << "e axis: ";
  for (size_t i = 0; i< NEBBS; i++) {
    e[i] = ei - ef[i];
    std::cout << e[i] << ", ";
  }
  std::cout << std::endl;

  DGTS_RebinTof2E<double, const double *, const double *,
    double *, double *> \
    rebinner( ei, mod2sample );

  rebinner.set_distance( distance );

  rebinner( tof, tof+NTOFBBS, Itof,
	    tmpe, 
	    e, e+NEBBS, Ie
	    );

  printVector( "tof = " , tof, tof+NTOFBBS);
  printVector( "tmpe = " , tmpe, tmpe+NTOFBBS);

  // try to use jacobian to do rebin and compare to the results of rebinner
  //   1. we need deOverdtof
  double deOverdtof = def/dtof;
  double jacobi[NEBINS];
  for (size_t i=0; i<NEBINS; i++) {
    double efc = (ef[i]+ef[i+1])/2;
    double vf = sqrt( efc ) * 437.3949;
    double tof = distance/vf*1000.;
    jacobi[i] = tof/2./efc * deOverdtof;
  }

  // compare
  std::cout << "compare rebinned intensity to Jacobi:" << std::endl;
  for (size_t i=0; i<NEBINS; i++) {
    std::cout << Ie[i] << ", " << jacobi[i] << std::endl;
    assert( std::abs((Ie[i]-jacobi[i])/Ie[i]) < 0.04 );
  }

  std::cout << "test2 done." << std::endl;
  return ;
}



// version
// $Id$

// End of file 
