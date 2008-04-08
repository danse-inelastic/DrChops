#include <iostream>
#include "../../libreduction/VanPlateAbsorp.h"


int main()
{
  using namespace DANSE::Reduction;

  VanPlateAbsorp test( 135.0 );
  double energy = 75; 
  
  for (double angle = 0.; angle<180; angle+=1.0) {
    std::cout << "angle: " << angle
	      << "abs:   " << test( angle*3.14159/180, energy )
	      << std::endl;
  }
  std::cout << "Test of VanTxCalcor passed" << std::endl;
  return 0;
}
