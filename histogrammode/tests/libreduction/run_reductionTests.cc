// T. M. Kelley tkelley@caltech.edu (c) 2004-2005

#include "run_reductionTests.h"

#include "reductionTest_EBinCalcor.h"
#include "reductionTest_ERebinAllInOne.h"
#include "reductionTest_He3DetEffic.h"

#include <iostream>
#include "journal/info.h"
#include "journal/debug.h"
#include "testFrame.h"
#include "reporting.h"

namespace ReductionTest
{
    bool run_reductionTests()
    {
        using journal::at;
        using journal::endl;
        using ARCSTest::testFrame;
        journal::info_t log("ReductionTest");
    

        bool EBinCalcorOK = testFrame( "EBinCalcor", "", log, 
                                        test_EBinCalcor);

        bool ERebinAllInOneOK = testFrame( "ERebinAllInOne", "", log, 
                                        test_ERebinAllInOne);

        bool He3DetEfficOK = testFrame( "He3DetEffic", "", log, 
                                        test_He3DetEffic);

        bool allPassed = 
            EBinCalcorOK && 
            ERebinAllInOneOK &&
            He3DetEfficOK ;
        return allPassed;
    } // run_reductionTests

} // ReductionTest::


// version
// $Id: run_reductionTests.cc 524 2005-07-11 20:44:02Z tim $

// End of file
