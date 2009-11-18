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
#include "drchops/Zt2Zxy.h"


void test();


int main()
{
   journal::debug_t debug2(DANSE::Reduction::Zt2Zxy_impl::jrnltag);
  debug2.activate();

  test();
  //test2();
}


void test()
{
  using namespace DANSE::Reduction;

  typedef std::vector<double> dblarr; typedef dblarr::iterator dblIt;
  typedef std::vector<bool> boolarr; typedef boolarr::iterator boolIt;

  size_t nt = 1000, nx=10, ny=15;

  // inputs
  dblarr 
    xt(nt), yt(nt), zt(nt);
  boolarr mask(nt);

  // z(t)
  std::cout << "preparing x(t), y(t), z(t), mask(t) ..." << std::endl;
  for (size_t t=0; t<nt; t++) {
    xt[t] = t/100;
    yt[t] = t*t/50000;
    zt[t] = 1;
    mask[t] = 0;
  }

  // prepare containers for the output z(x,y)
  dblarr outxbb(nx), outybb(ny);
  for (size_t x=0; x<nx; x++) outxbb[x] = x;
  for (size_t y=0; y<ny; y++) outybb[y] = y;
  dblarr zxy(nx*ny);
  
  std::cout << "Preparation of data finished. Start reduction..." << std::endl;
  
  // reduction
  Zt2Zxy <double, double, double, dblIt, dblIt, dblIt, boolIt, dblIt, dblIt, dblIt>
    (xt.begin(), yt.begin(), zt.begin(), mask.begin(), nt,
     outxbb.begin(), outxbb.end(), outybb.begin(), outybb.end(),
     zxy.begin());
  
  std::cout << "testZt2Zxy_batch done." << std::endl;

  for (size_t i=0; i<nx-1; i++) {
    for (size_t j=0; j<ny-1; j++) 
      std::cout << zxy[i*(ny-1)+j] << ", ";
    std::cout << std::endl;
  }
  return ;
}



// version
// $Id$

// End of file 
