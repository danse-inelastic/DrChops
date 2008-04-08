// T. M. Kelley tkelley@caltech.edu (c) 2004

#include "He3DetEffic.h"

#include "reductionTest_He3DetEffic.h"
#include "testFrame.h"
//#include "compareVectors.h"
#include "journal/info.h"
#include "journal/debug.h"


namespace
{
    char journalname [] = "ReductionTest";

    using journal::at;
    using journal::endl;
    using journal::newline;
}


namespace ReductionTest
{
    using namespace ARCSTest;
    namespace he3DetEffic
    {
        char target[] = "He3DetEffic";
        char aspect1[] = "instantiate";
    }

    bool test_He3DetEffic()
    {
        journal::info_t info( journalname);

        using namespace he3DetEffic;

        info << journal::at(__HERE__) << journal::endl;

        bool passed1 = 
            testFrame( target, aspect1, info, he3DetEffic::test_1);

        info << journal::endl;
        return passed1;
    }

    namespace he3DetEffic
    {
        bool test_1()
        {
            journal::info_t info( journalname);
            
            using namespace Reduction;

            He3DetEffic< double> hdd( 10.0);
            info << at(__HERE__);
            info << "instantiated He3DetEffic<double>" << newline;

            He3DetEffic< float> hdf( 10.0);
            info << at(__HERE__) << "instantiated He3DetEffic<float>" 
                 << newline;

            He3DetEffic< double, std::vector<double>::iterator> hddvit( 10.0);
            info << at(__HERE__) << "instantiated He3DetEffic<double, "
                 << "std::vector<double>::iterator>" << newline;

            He3DetEffic< float, std::vector<float>::iterator> hdfvit( 10.0);
            info << at(__HERE__) << "instantiated He3DetEffic<float, "
                 << "std::vector<float>::iterator>" << newline;

            He3DetEffic< float, std::vector<double>::iterator> hdfvdit( 10.0);
            info << at(__HERE__) << "instantiated He3DetEffic<float, "
                 << "std::vector<double>::iterator>--not that it's a good "
                 << "idea, just wanted to see if it could be done" << newline;

            info << endl;

            return true;
        } // test_1

    } // he3DetEffic::

} // ReductionTest::



// version
// $Id: reductionTest_He3DetEffic.cc 416 2005-05-12 15:14:33Z tim $

// End of file
