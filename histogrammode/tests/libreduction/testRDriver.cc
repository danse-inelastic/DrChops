#include <iostream>
#include "../../libreduction/RDriver.h"
#include "journal/debug.h"


int main()
{
  journal::debug_t debug("RDriver");
  debug.activate();

  using namespace DANSE::Reduction;

  typedef std::vector<float> VecF;
  VecF speHist(90), phiBB(9);
  size_t otherArrLen = 10;
  
  RDriver<float> rdriver(speHist, otherArrLen, phiBB);

  std::cout << "test of RDriver passed " << std::endl;
  return 0;
}
