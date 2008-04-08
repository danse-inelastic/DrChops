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
#include "reduction/tof2E.h"


using namespace DANSE::Reduction;

void test_tof2E1();
void test_tof2E2();

int main()
{
  test_tof2E1();
  test_tof2E2();
}

void test_tof2E1()
{
  double distance = 10000, tof = 3000.;

  double e = tof2E( tof, distance ) ;

  double expected = DANSE::Physics::Units::Conversion::v2E( distance/tof*1000. );
  
  assert( (e-expected)/expected < 1.e-7 );
}

void test_tof2E2()
{
  double distance=10000, tof[10], e[10];
  
  for (size_t i=0; i<10; i++) 
    tof[i] = 3000. + 100 * i;

  tof2E( tof, tof+10, distance, e );

  for (size_t i=0; i<10; i++) {

    double expected = DANSE::Physics::Units::Conversion::v2E
      (distance/tof[i]*1000. );
    assert( (e[i]-expected)/expected < 1.e-7 );

  }
}

// version
// $Id$

// End of file 
