// T. M. Kelley tkelley@caltech.edu (c) 2004

#include <iostream>

#include <vector>

#include "reduction/He3DetEffic.h"

#include "journal/info.h"
#include "journal/debug.h"


namespace
{
    char journalname [] = "ReductionTest";

    using journal::at;
    using journal::endl;
    using journal::newline;

  void report(const char * name, bool passed)
  {
    std::cout << "-> " << name ;
    if (passed) std::cout << " passed.";
    else std::cout << " failed.";
    std::cout << std::endl;
  }

}


namespace ReductionTest
{

    namespace he3DetEffic
    {
        bool test_1()
        {
            journal::info_t info( journalname);
            
            using namespace DANSE::Reduction;

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

        bool _test_2(double pressure, double radius, int n, double costheta,
		     double energy)
        {
            journal::info_t info( journalname);
            
            using namespace DANSE::Reduction;

            He3DetEffic< double> hdd( pressure, radius, n, costheta);
            info << at(__HERE__);
            info << "instantiated He3DetEffic<double>(pressure=" << pressure 
		 << ", radius=" << radius
		 << ", n=" << n
		 << ", costheta=" << costheta
		 << newline;

	    info << "effciency at " << energy << " is " << hdd(energy ) << endl;
	    return true;
	}

        bool test_2()
        {
	  _test_2( 10.0, 1.27, 1, 1., 47.043);
	  _test_2( 10.0, 1.27, 1, 0.8, 47.043);
	  return true;
	}

        bool test_3()
        {
	  _test_2( 10.0, 1.27, 200, 1., 47.043);
	  _test_2( 6.0, 1.27, 200, 1., 47.043);
	  return true;
	}

        bool test_4()
        {

            journal::info_t info( journalname);
            
            using namespace DANSE::Reduction;

	    double pressure=10.0, radius = 1.27;
	    int n = 200;

            He3DetEffic<double, std::vector<double>::iterator> hdd( pressure, radius, n);
            info << at(__HERE__);
            info << "instantiated He3DetEffic<double>(pressure=" 
		 << pressure 
		 << ", radius=" 
		 << radius
		 << ", n="
		 << n
		 << newline;

	    std::vector<double> energies(5);
	    for (int i=0; i<5; i++) 
	      energies[i] = 50 + i*4;

	    std::vector<double> efficiencies(5);
	    hdd( energies.begin(), efficiencies.begin(), efficiencies.end() );

	    for (int i=0; i<5; i++)
	      info << "effciency at " << energies[i]
		   << " is " << efficiencies[i] << endl;

	    return true;
	}

    } // he3DetEffic::


    bool test_He3DetEffic()
    {
        journal::info_t info( journalname);
	info.activate();

        using namespace he3DetEffic;

        info << journal::at(__HERE__) << journal::endl;

        bool passed1 = he3DetEffic::test_1(); report ("test1", passed1);
	bool passed2 = he3DetEffic::test_2(); report ("test2", passed2);
        bool passed3 = he3DetEffic::test_3(); report ("test3", passed3);
        bool passed4 = he3DetEffic::test_4(); report ("test4", passed4);

        info << journal::endl;
        return passed1 and passed2 and passed3 and passed4 ;
    }

} // ReductionTest::


int main()
{
  journal::debug_t debug( "he3deteffic" );
  debug.activate();
  bool passed = ReductionTest::test_He3DetEffic(); 
  report ("test of He3DetEffic", passed );
}

// version
// $Id: reductionTest_He3DetEffic.cc 416 2005-05-12 15:14:33Z tim $

// End of file
