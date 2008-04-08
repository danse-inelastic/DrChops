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
#include "reduction/Universal1DRebinner.h"


#include "reduction/tof2E.h"

void test_tof2E();
void test_trivial();



int main()
{
  journal::debug_t debug( DANSE::Reduction::Universal1DRebinner_Impl::jrnltag );
  debug.activate();
  
  test_trivial();
  test_tof2E();
}


void test_tof2E()
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
  
  class Tof2E: public Functor<double, double> {
  public:
    Tof2E( double distance ) 
      : m_distance(distance)
    {}
    
    virtual double operator() ( const double & tof ) {
      return tof2E( tof, m_distance );
    }
    ~Tof2E() {}
    
  private:
    double m_distance;
  };
  

  Tof2E tof2E( distance );
  
  Universal1DRebinner
    <
  double, 
    const double*, 
    double,
    const double*, 
    double, 
    double*,
    double,
    double*
    > rebinner;
  
  rebinner( tof, tof+10, Itof,
	    tmpe, 
	    e, e+10, Ie,
	    tof2E
	    );
  
  double sum = 0;
  for (size_t i=0; i<9; i++) {
    std::cout << Ie[i] << std::endl;
    sum += Ie[i];
  }
  assert ( (sum-9)/9 < 1e-7 );
  
  for (size_t i =0; i<100; i++)
    rebinner( tof, tof+10, Itof,
	      tmpe, 
	      e, e+10, Ie,
	      tof2E
	      );
  
  return ;
}



void test_trivial()
{
  double x[11], Ix[10], y[22], Iy[21], tmpy[21];
  
  for (size_t i=0; i<11; i++) {
    x[i] = i;
    if (i < 10) Ix[i] = 1.0;
  }
  
  for (size_t i=0; i<22; i++) {
    y[i] = i;
    if (i<21) Iy[i] = 0;
  }
  
  using namespace DANSE::Reduction;
  
  class Scale: public Functor<double, double> {
  public:
    Scale( double scale_factor ) 
      : m_scale_factor(scale_factor)
    {}
    
    virtual double operator() ( const double & x ) {
      return m_scale_factor * x;
    }
    
  private:
    double m_scale_factor;
  };
  
  Scale f(2);
  
  Universal1DRebinner<
  double, 
    const double*, 
    double,
    const double*, 
    double, 
    double*,
    double,
    double*
    > rebinner;
  
  rebinner( x, x+11, Ix,
	    tmpy,
	    y, y+21, Iy,
	    f);
  
  for (size_t i=0; i<22; i++) {
    assert ( Iy[i] * 2 - 1 < 1e-7 );
  }
  return ;
}


// version
// $Id$

// End of file 
