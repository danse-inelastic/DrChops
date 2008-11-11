// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_REDUCTION_HISTOGRAMMER
#define H_REDUCTION_HISTOGRAMMER

#include "histogram/OutOfBound.h"
#include "journal/warning.h"

namespace DANSE{ namespace Reduction {

    using namespace DANSE::Histogram;
    
    /// Histogammer1: add an entity to a 1D histogram I(x).
    /// Class to add an entity 
    /// to a 1-D histogram (object of GridData_1D).
    /// The operator Get is responsible to calculate x,I value of the entity,
    /// 
    /// template arguments:
    ///   GridData_1D: I(x) histogram. 1-dimensional
    ///   Entity: type of the entity to be added to I(x)
    ///   Get: map entity to x, I
    ///   XDataType: data type of x
    ///   IDataType: data type of I
    template <typename Entity, typename GridData_1D, 
	      typename Get,
	      typename XDataType, typename IDataType>
    class Histogrammer1 {
    
    public:
      Histogrammer1( GridData_1D & Ix, const Get & e2xI)
	: m_Ix(Ix), m_e2xI(e2xI)
      {
      }
    
      void operator() ( const Entity & e )
      {
	// calculate x, I from e
	m_e2xI(e, m_x, m_I);

	// add to the histogram
	try {
	  m_Ix( m_x ) += m_I;
	}
	catch (OutOfBound err)  {
#ifdef DEBUG
	  journal::warning_t warning("reduction.Histogrammer1");
	  warning << journal::at(__HERE__)
		  << "OutOfBound: " << err.what()
		  << journal::endl;
#endif
	}
      }
    
    private:
      GridData_1D & m_Ix;
      const Get & m_e2xI;
      XDataType m_x;
      IDataType m_I;
    };


    /// Histogammer2: add an entity to a 2D histogram I(x,y).
    /// Class to add an entity
    /// to a 2-D histogram (object of GridData_2D).
    /// 
    /// template arguments:
    ///   GridData_2D: I(x,y) histogram.
    ///   Entity: type of the entity to be added to I(x)
    ///   Get: map entity to x, y, I
    ///   XDataType: data type of x
    ///   YDataType: data type of y
    ///   IDataType: data type of I
    ///
    template <typename Entity, typename GridData_2D, 
	      typename Get,
	      typename XDataType, typename YDataType, typename IDataType>
    class Histogrammer2 {
    
    public:
      Histogrammer2( GridData_2D & Ixy, const Get & e2xyI )
	: m_Ixy( Ixy ), m_e2xyI( e2xyI )
      {
      }
    
      void operator() ( const Entity & e )
      {
	// calculate x, I from e
	m_e2xyI(e, m_x, m_y, m_I);

	// add to histogram
	try {
	  m_Ixy( m_x, m_y ) += m_I;
	}
	catch (OutOfBound err)  {
#ifdef DEBUG
	  journal::warning_t warning("reduction.Histogrammer2");
	  warning << journal::at(__HERE__)
		  << "OutOfBound: " << err.what()
		  << journal::endl;
#endif
	}
      }
    
    private:
      GridData_2D & m_Ixy;
      const Get & m_e2xyI;
      XDataType m_x;
      YDataType m_y;
      IDataType m_I;
    };


    /// Histogammer4: add an entity to a 4D histogram I(x1,x2,x3,x4).
    ///
    /// template arguments:
    ///   GridData_4D: I(x1,x2,x3,x4) histogram. 
    ///   Get: map entity to x1,x2,x3,x4, I
    ///   X1DataType: data type of x1
    ///   X2DataType: data type of x2
    ///   X3DataType: data type of x3
    ///   X4DataType: data type of x4
    ///   IDataType: data type of I
    ///
    template <typename Entity, typename GridData_4D, typename Get, 
	      typename X1DataType, typename X2DataType, 
	      typename X3DataType, typename X4DataType,
	      typename IDataType>
    class Histogrammer4 {
      
    public:
      Histogrammer4( GridData_4D & Ixxxx, const Get & e2xI )
	: m_Ixxxx( Ixxxx ), m_e2xI( e2xI )
      {
      }
      
      void operator() ( const Entity & e )
      {
	// calculate x, I from e
	m_e2xI(e, m_x1, m_x2, m_x3, m_x4, m_I);
	
	// add to histogram
	try {
	  m_Ixxxx( m_x1, m_x2, m_x3, m_x4 ) += m_I;
	}
	catch (OutOfBound err)  {
#ifdef DEBUG
	  journal::warning_t warning("reduction.Histogrammer4");
	  warning << journal::at(__HERE__)
		  << "OutOfBound: " << err.what()
		  << journal::endl;
#endif
	}
      }
      
    private:
      GridData_4D & m_Ixxxx;
      const Get & m_e2xI;
      X1DataType m_x1;
      X2DataType m_x2;
      X3DataType m_x3;
      X4DataType m_x4;
      IDataType m_I;
    } ;

  }} // DANSE::Reduction


#endif // H_REDUCTION_HISTOGRAMMER


// version
// $Id$

// End of file 
