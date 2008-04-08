// T. M. Kelley tkelley@caltech.edu (c) 2004

#include "reductionTest_ERebinAllInOne.h"
#include "ERebinAllInOne.h"
#include "EBinCalcor.h"
//#include "PharosPixel.h"

#include "testFrame.h"
#include "compareVectors.h"
#include "journal/info.h"
#include "journal/debug.h"

#include <vector>
#include <iostream>


namespace
{
    char journalname [] = "ReductionTest";

    using journal::at;
    using journal::endl;

    typedef std::vector<double> vecdub;
    typedef std::vector<float> vecfloat;
    typedef std::vector<double>::size_type vdsz;
    typedef std::vector<float>::size_type vfsz;
}

namespace ReductionTest
{
    using namespace ARCSTest;
    namespace eRebinAllInOne
    {
        char target[] = "ERebinAllInOne";
        char aspect1[] = "Instantiation, FPT=double";
        char aspect2[] = "Instantiation, FPT=float";
        char aspect3[] = "Instantiation, FPT=double, VT=std::vector<double>";
        char aspect4[] = "Instantiation, FPT=double, VT=std::vector<float>";
        char aspect5[] = "Instantiation, FPT=double, VT=std::vector<double>, SzT= std::vector<double>::size_t";
        char aspect6[] = "Instantiation, FPT=double, VT=std::vector<float>, SzT=std::vector<float>::size_type";
        char aspect7[] = "call, using identical bins, FPT=double, VT=std::vector<float>, SzT=std::vector<float>::size_type";
        char aspect8[] = "call, using nonoverlapping bins, FPT=double, VT=std::vector<float>, SzT=std::vector<float>::size_type";
        char aspect9[] = "call, using realistic pixel, FPT=double, VT=std::vector<float>, SzT=std::vector<float>::size_type";
    }

    bool test_ERebinAllInOne()
    {
        journal::info_t info( journalname);

        using namespace eRebinAllInOne;

        info << journal::at(__HERE__) << journal::endl;

        bool passed1 = 
            testFrame( target, aspect1, info, eRebinAllInOne::test_1);

        bool passed2 = 
            testFrame( target, aspect2, info, eRebinAllInOne::test_2);

        info << journal::at(__HERE__) << journal::endl;

        bool passed3 = 
            testFrame( target, aspect3, info, eRebinAllInOne::test_3);

        info << journal::at(__HERE__) << journal::endl;

        bool passed4 = 
            testFrame( target, aspect4, info, eRebinAllInOne::test_4);

        bool passed5 = 
            testFrame( target, aspect5, info, eRebinAllInOne::test_5);

        info << journal::at(__HERE__) << journal::endl;

        bool passed6 = 
            testFrame( target, aspect6, info, eRebinAllInOne::test_6);

        info << journal::at(__HERE__) << journal::endl;

        bool passed7 = 
            testFrame( target, aspect7, info, eRebinAllInOne::test_7);

        info << journal::at(__HERE__) << journal::endl;

        bool passed8 = 
            testFrame( target, aspect8, info, eRebinAllInOne::test_8);

        info << journal::at(__HERE__) << journal::endl;

        bool passed9 = 
            testFrame( target, aspect9, info, eRebinAllInOne::test_9);

        info << journal::endl;
        return passed1 && passed2 && passed3 && passed4 && passed5 && passed6 && passed7 && passed8 && passed9;
    }

    namespace eRebinAllInOne
    {
        bool test_1()    // instantiation
        {
            Reduction::ERebinAllInOne<double> test( 10, 10, 1.0);
            return true;
        } // test_1()


        bool test_2()    // instantiation
        {
            Reduction::ERebinAllInOne<double> test( 10, 10, 1.0);
            return true;
        } // test_2()


        bool test_3()    // instantiation
        {
            Reduction::ERebinAllInOne<double, vecdub> test( 10, 10, 1.0);
            return true;
        } // test_3()


        bool test_4()    // instantiation
        {
            Reduction::ERebinAllInOne<float, vecfloat> test( 10, 10, 1.0);
            return true;
        } // test_4()


        bool test_5()    // instantiation
        {
            Reduction::ERebinAllInOne<double, vecdub, vdsz> test( 10, 10, 1.0);
            return true;
        } // test_5()


        bool test_6()    // instantiation
        {
            Reduction::ERebinAllInOne<float, vecfloat,vfsz> test( 10, 10, 1.0);
            return true;
        } // test_6()


        bool test_7()    // call, identical bins
        {
            journal::info_t info("RebinTest");

            double barray[] = {0.0, 1.0, 2.0, 3.0, 4.0};
            vecdub oldBounds( &barray[0], &barray[5]);
            vecdub newBounds( &barray[0], &barray[5]);

            Reduction::ERebinAllInOne<double, vecdub, vdsz> test( 4, 4, 1.0);
            
            vecdub indata( 4, 1.0), inerrs( 4, 1.0);
            vecdub outdata( 4, 0.0), outerrs(4,0.0);

            test( oldBounds, newBounds, indata, inerrs, outdata, outerrs);

            vecdub expctd( 4, 1.0);

            info << journal::at(__HERE__) << "testing indata";
            bool p1 = compareFPVectors<double>( indata, expctd, 1.e-10, info);
            info << "testing inerrs"; info.newline();
            bool p2 = compareFPVectors<double>( inerrs, expctd, 1.e-10, info);
            info << "testing outdata"; info.newline();
            bool p3 = compareFPVectors<double>( outdata, expctd, 1.e-10, info);
            info << "testing outerrs"; info.newline();
            bool p4 = compareFPVectors<double>( outerrs, expctd, 1.e-10, info);
            info << journal::endl;

            return p1 && p2 && p3 && p4;
        } // test_7()




        bool test_8()     // call, non-overlapping bins
        {
            journal::info_t info("RebinTest");

            double barray1[] = {0.0, 1.0, 2.0, 3.0, 4.0};
            vecdub oldBounds( &barray1[0], &barray1[5]);
            double barray2[] = {10.0, 11.0, 12.0, 13.0, 14.0};
            vecdub newBounds( &barray2[0], &barray2[5]);

            Reduction::ERebinAllInOne<double, vecdub, vdsz> test( 4, 4, 1.0);

            vecdub indata( 4, 1.0), inerrs( 4, 1.0);
            vecdub outdata( 4, 0.0), outerrs(4,0.0);

            test( oldBounds, newBounds, indata, inerrs, outdata, outerrs);

            vecdub expctd( 4, 0.0);

            info << journal::at(__HERE__) << "testing outdata"; info.newline();
            bool p1 = compareFPVectors<double>( outdata, expctd, 1.e-10, info);
            info << "testing outerrs"; info.newline();
            bool p2 = compareFPVectors<double>( outerrs, expctd, 1.e-10, info);
            info << journal::endl;

            return p1 && p2;
        } // test_8()


        bool test_9()     // call, realistic pixel
        {
            journal::info_t info("RebinTest");

            
            std::vector<double> tbb(10);
            std::vector<double> ebbn(10);

            double deltaT = 50.0;
            for( size_t i=0; i<tbb.size(); i++) tbb[i] = 3000.0 + deltaT*i;
            for( size_t i=0; i<ebbn.size(); i++) ebbn[i] = -50.0 + 10.0*i;

            Reduction::EBinCalcor<double> ebcalc( 276.5, 20100.0);
            std::vector<double> ebbo(10);
            double distance = std::sqrt( 4000.0*4000.0 + 0.05*0.05);
            ebcalc( distance, tbb, ebbo);

            Reduction::ERebinAllInOne<double, vecdub, vdsz> test( 9, 9, 5.0, false, 276.5);

            vecdub indata( 9, 1.0), inerrs( 9, 1.0);
            vecdub outdata( 9, 0.0), outerrs(9,0.0);

            test( ebbo, ebbn, indata, inerrs, outdata, outerrs);

            double refArray[] = {0.7958087239, 0.7958087239, 0.7958087239, 
                                 0.9031594330, 1.0536518999, 1.0536518999, 
                                 1.0536518999, 1.0536518999, 1.2604285222};
            std::vector<double> expctd( &refArray[0], &refArray[9]);

            double tol = 1.e-10;

            info << journal::at(__HERE__) << "testing outdata"; info.newline();
            bool p1 = compareFPVectors<double>( outdata, expctd, tol, info);
            info << "testing outerrs"; info.newline();
            bool p2 = compareFPVectors<double>( outerrs, expctd, tol, info);
            info << journal::endl;

            std::cout.precision(11);
            std::cout.setf( std::ios_base::showpoint);

            if (!p1)
            {
                for (size_t i = 0; i < outdata.size(); ++i)
                {
                    std::cout << outdata[i] << "\n";
                }
            }

            return p1 && p2;
        } // test_9()


    } // eRebinAllInOne::

} // ReductionTest::



// version
// $Id: reductionTest_ERebinAllInOne.cc 524 2005-07-11 20:44:02Z tim $

// End of file
