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
#include <iostream>
#include "reduction/ReverseIterator.h"


void test();

int main()
{
  test();
}

void test()
{
  using namespace DANSE;


  double a[10];
  for (size_t i=0; i<10; i++) a[i] = i;
  
  typedef ReverseIterator< double *, double > RIT;

  RIT rbegin(a+9), rend(a-1);

  for (RIT rit = rbegin; rit<rend; rit++) {

    assert ( *rit == 9 - (rit-rbegin) );
  }

  double b = *(rbegin+3), c = *(rend-3);
  
  RIT rit1(rbegin);

  rit1 ++;  ++rit1;
  rit1 --;  --rit1;
  
}

// version
// $Id$

// End of file 
