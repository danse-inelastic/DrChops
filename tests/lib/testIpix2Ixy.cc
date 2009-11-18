// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                      (C) 2007-2009  All Rights Reserved
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
#include "drchops/Ipix2Ixy.h"


void test();


int main()
{
   journal::debug_t debug2(DANSE::Reduction::Ipix2Ixy_impl::jrnltag);
  debug2.activate();

  test();
  //test2();
}


template <typename iterator_t>
void printIxy(iterator_t it, size_t nx, size_t ny) {
  for (size_t i=0; i<nx; i++) {
    for (size_t j=0; j<ny; j++) 
      std::cout << *(it+i*ny+j) << ", ";
    std::cout << std::endl;
  }
}


void test()
{
  using namespace DANSE::Reduction;

  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  size_t np = 1000, nx=10, ny=15;

  // inputs
  dblarr 
    xp(np), yp(np), Ip(np), IE2p(np), sap(np), saE2p(np);
  boolarr mask(np);

  std::cout << "preparing x(pixel), y(pixel), I(pixel) ..." << std::endl;
  for (size_t p=0; p<np; p++) {
    xp[p] = p/100;
    yp[p] = p*p/50000;
    Ip[p] = 1;
    sap[p] = 1;
    mask[p] = 0;
  }

  // prepare conpainers for the output z(x,y)
  dblarr outxbb(nx), outybb(ny);
  for (size_t x=0; x<nx; x++) outxbb[x] = x;
  for (size_t y=0; y<ny; y++) outybb[y] = y;
  dblarr outIxy(nx*ny), outIE2xy(nx*ny), outsaxy(nx*ny), outsaE2xy(nx*ny);
  
  std::cout << "Preparation of data finished. Start reduction..." << std::endl;
  
  // reduction
  Ipix2Ixy <double, double, dblIt, dblIt, dblIt, dblIt, boolIt, dblIt, dblIt>
    (xp.begin(), yp.begin(), Ip.begin(), IE2p.begin(), sap.begin(), saE2p.begin(),
     mask.begin(), np,
     outxbb.begin(), outxbb.end(), outybb.begin(), outybb.end(),
     outIxy.begin(), outIE2xy.begin(), outsaxy.begin(), outsaE2xy.begin()
     );
  
  std::cout << "testIpix2Ixy_batch done." << std::endl;

  std::cout << "I(x,y)" << std::endl;
  printIxy<dblIt>(outIxy.begin(), nx-1, ny-1);
  std::cout << std::endl;

  std::cout << "Solidangle(x,y)" << std::endl;
  printIxy<dblIt>(outsaxy.begin(), nx-1, ny-1);

  return ;
}

// version
// $Id$

// End of file 
