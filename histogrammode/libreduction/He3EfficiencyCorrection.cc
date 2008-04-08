//#include <iostream>
#include "He3EfficiencyCorrection.h"

namespace DANSE { namespace Reduction{

    namespace He3EfficiencyCorrection_impl{
      const char * jrnltag = "He3EfficiencyCorrection";
    } // He3EfficiencyCorrection_impl

    //explicit instantiations    
    template class He3EfficiencyCorrection<double, std::vector<double>::iterator >;

  } // Reduction:
} // DANSE:

