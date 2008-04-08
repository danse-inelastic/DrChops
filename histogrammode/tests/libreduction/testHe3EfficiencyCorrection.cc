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

#include <iostream>
#include <vector>

#include "journal/info.h"
#include "reduction/He3EfficiencyCorrection.h"


int test1()
{
  typedef std::vector<double> Vec;

  Vec energies(10);
  for (size_t i=0; i<10; i++) energies[i] = 40 + 2*i;
  
  using namespace DANSE::Reduction;

  He3EfficiencyCorrection<double, Vec::iterator> corrector( energies.begin(), energies.end() );

  Vec intensities(10);
  for (size_t i=0; i<10; i++) intensities[i] = 1.;
  corrector.correct( intensities.begin(), 10, 1.27 );

  journal::info_t info("He3EfficiencyCorrection_test1");
  info.activate();
  
  info << "corrected intensities:" << journal::newline;
  for (size_t i=0; i<10; i++) {
    info << intensities[i] << ", ";
  }
  info << journal::endl;

  return 0;
}


int test2()
{
  typedef std::vector<double> Vec;

  Vec energies(10);
  for (size_t i=0; i<10; i++) energies[i] = 40 + 2*i;
  
  using namespace DANSE::Reduction;

  He3EfficiencyCorrection<double, Vec::iterator> corrector( energies.begin(), energies.end() );

  Vec intensities(10);
  for (size_t i=0; i<10; i++) intensities[i] = 1.;

  for (size_t pixel=0; pixel < 1000000; pixel++) {
    corrector.correct( intensities.begin(), 10, 1.27 );
  }

  return 0;
}


int main()
{
  test1();
  test2();
}

// version
// $Id: reductionTest_He3DetEffic.cc 416 2005-05-12 15:14:33Z tim $

// End of file
