// T. M. Kelley tkelley@caltech.edu (c) 2004

#include "journal/info.h"
#include "run_reductionTests.h"

int main( int argc, char **argv)
{
    journal::info_t info("ReductionTest");
    info.activate();
    bool allPassed = ReductionTest::run_reductionTests();

    info << journal::at(__HERE__); info.newline();
    if (allPassed) 
        info << "All tests of reduction PASSED" << journal::endl;
    else 
        info << "Some test(s) reduction FAILED" << journal::endl;
    return 0;
}


// version
// $Id: main.cc 416 2005-05-12 15:14:33Z tim $

// End of file
