// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2003-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#ifndef DANSE_REDUCTION_VANPLATEABSORP_H
#define DANSE_REDUCTION_VANPLATEABSORP_H


// #ifndef CMATH_INCLUDED
// #define CMATH_INCLUDED
// #include <cmath>
// #endif

#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif

namespace DANSE{
  namespace Reduction {
    
    /// functor that computes the transmission of neutrons of a 
    /// specified energy scattered toward a detector through 
    /// a flat plate of vanadium. 
    class VanPlateAbsorp
    {
      typedef std::vector<double> VecDub;
    public:
      /// detector angle in radians
      /// energy in meV
      double operator()( double detAngle, double energy);
      
      /// darkAngle is the angle between plate's long axis, meas. from 
      ///     transmitted beam, in degrees.
      /// thickness and width of plate in cm
      explicit VanPlateAbsorp( double darkAngle, 
			       double thickness=0.2, 
			       double width=6.3);
    private:
      double m_pi;
      double m_darkAng;     /// dark angle of plate
      double m_darkAngRad;  /// dark angle of plate in radians
      double m_th;          /// thickness, cm
      double m_w;           /// width, cm
      /// geometry for abs calc:
      double m_dt;   /// delta-plate-thickness
      double m_dw;   /// delta-plate-width
      int m_ntpts;   /// # thickness points
      int m_nwpts;   /// # width points
      double m_norm; /// 1/(# t points*# w points)
      VecDub m_y;    /// x-coordinates of cells
      VecDub m_x;    /// y-coordinates of cells
      VecDub m_li;   /// incident path lengths
      VecDub m_th1;  /// angles
      VecDub m_th2;
      /// constants
      double m_mu_scatt;    /// sig_scatt*rho*NAv/mass scatt x_sect per c.c.
      double m_mu_abs;      /// abs x section per cubic cm
    };
  } // Reduction::
} // DANSE::

#endif // DANSE_REDUCTION_VANPLATEABSORP_H



// version
// $Id: VanPlateAbsorp.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
