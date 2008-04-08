// T. M. Kelley tkelley@caltech.edu (c) 2004

#include "reductionTest_EBinCalcor.h"
#include "reduction/EBinCalcor.h"
#include <cmath>

#include "testFrame.h"
#include "compareVectors.h"
#include "journal/info.h"
#include "journal/debug.h"

namespace
{
    char journalname [] = "ReductionTest";

    using journal::at;
    using journal::endl;
}

namespace ReductionTest
{
    using namespace ARCSTest;
    namespace eBinCalcor
    {
        char target[] = "Reduction::EBinCalcor";
        char aspect1[] = "ctor";
        char aspect2[] = "operator()";
    }

    bool test_EBinCalcor()
    {
        journal::info_t info( journalname);

        using namespace eBinCalcor;

        info << journal::at(__HERE__) << journal::endl;

        bool passed1 = 
            testFrame( target, aspect1, info, eBinCalcor::test_1);

//         info << journal::at(__HERE__) << journal::endl;

//         bool passed2 = 
//             testFrame( target, aspect2, info, eBinCalcor::test_2);

        info << journal::endl;
        return passed1;// && passed2;
    }

    namespace eBinCalcor
    {
        bool test_1()
        {
            double mod2sampDist = 20100.0;
            double incidentE = 276.5;
            Reduction::EBinCalcor<double> ebc( incidentE, mod2sampDist);
            return true;
        } // test_1


        bool test_2()
        {
            journal::info_t info( journalname);

            // time bins
            std::vector<double> tbb( 10,0.0);
            for(size_t i=0; i<10; ++i) tbb[i] = 3000.0 + 50.0*i;

            // create e bin calcor
            double mod2sampDist = 20100.0;
            double incidentE = 276.5;
            Reduction::EBinCalcor<double> ebc( incidentE, mod2sampDist);

            double pixelDistance = std::sqrt(4000.0*4000.0 + 0.05*0.05);

            // output
            std::vector< double> ebb(10,0.0);

            // execute
            ebc( pixelDistance, tbb, ebb);

            // evaluate
            double refArray[] = {-1219.97, -743.072, -462.515, -283.634,
                                 -162.634, -76.9926, -14.1634, 33.2906,
                                 70.0056, 98.9935};
            std::vector<double> expected( &refArray[0], &refArray[10]);
            return compareFPVectors( ebb, expected, 0.01, info);
        } // test_2


    } // eBinCalcor::

} // ReductionTest::



// version
// $Id: reductionTest_EBinCalcor.cc 524 2005-07-11 20:44:02Z tim $

// End of file
