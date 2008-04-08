// T. M. Kelley tkelley@caltech.edu (c) 2004
#ifndef REDUCTIONTEST_HE3DETEFFIC_H
#define REDUCTIONTEST_HE3DETEFFIC_H

namespace ReductionTest
{
    bool test_He3DetEffic();

    namespace he3DetEffic
    {
        extern char target[];

        bool test_1();
        extern char aspect1[];
        bool test_2();
        extern char aspect2[];
        bool test_3();
        extern char aspect3[];
    }
}

#endif



// version
// $Id: reductionTest_He3DetEffic.h 416 2005-05-12 15:14:33Z tim $

// End of file
