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


#include "VanPlateAbsorp.h"
#include <cmath>
#include <iostream>

namespace DANSE {
  namespace Reduction {
    
    double VanPlateAbsorp::operator()( double detAngle, double energy)
    {
      double abs = 0.0;
      double mu = m_mu_scatt + m_mu_abs*sqrt(25.3/energy);
      for(int i=0; i<( m_ntpts+1); i++)
        {
	  //			double y = m_dt*(i + 0.5f);
	  //			double li = y/cos( m_darkAngRad);
	  for(int j=0; j<( m_nwpts+1); j++)
            {
	      double lf = 0.0f;
	      //				double x = m_dw*(j+0.5f);
	      // 				double a = atan(y[i]/x[j]);
	      // 				double b = atan( (m_th-y[i])/x[j]);
	      // 				double th1 = m_darkAngRad - b;
	      // 				double th2 = m_darkAngRad + a;
	      int idx = i*( m_nwpts+1) + j;
	      
	      // lf is length of flight after scattering
	      if(detAngle <= m_th1[idx]) 
		lf = fabs( ( m_th - m_y[i])/
			   cos( m_pi*0.5 + detAngle - m_darkAngRad));
	      
	      else if(detAngle > m_th2[idx]) 
		lf = fabs( m_y[i]/cos( m_pi*0.5 -detAngle + m_darkAngRad) );
	      
	      else lf = m_x[j]/cos( detAngle-m_darkAngRad );
              
              
	      // 				if(lf < 0.0f) 
	      //				std::cout<<"white_van::calcAbs() x[j] = "<<x[j]
	      //						 <<"; y[i] = "<<y[i]<<"; li = "<<li<<"; lf = "<<lf<<"\n";
	      abs += expf( -mu*( m_li[i]+lf) );
            }
        }
      return abs*m_norm;
    } // operator()( ... )
    
    
    VanPlateAbsorp::VanPlateAbsorp( double darkAngle, 
                                    double thickness, 
                                    double width)
      : m_pi( 3.1415926535897932384626 ),
	m_darkAng( darkAngle),
	m_darkAngRad( darkAngle*m_pi/180.0),
	m_th( thickness),
	m_w( width),
	// geometry
	m_dt( 0.01),
	m_dw( 0.05),
	m_ntpts( (int)(m_th/m_dt)-1),
	m_nwpts( (int)(m_w/m_dw)-1),
	m_norm( static_cast<double>(1.0/((m_ntpts+1.0)*(m_nwpts+1.0)) ) ),
	m_y( m_ntpts+1),
	m_x( m_nwpts+1),
	m_li(m_ntpts+1),
	m_th1( (m_ntpts+1)*(m_nwpts+1)),
	m_th2( (m_ntpts+1)*(m_nwpts+1)),
	// constants
	// cross section * mass density * Avag's num / molar mass
	m_mu_scatt( 5.10e-24*5.499*6.022e23/50.942),
	m_mu_abs( 5.08e-24*5.499*6.022e23/50.942)
    {
      //std::cout << m_darkAng << "," << m_darkAngRad << "," << m_th << "," << m_w << std::endl;
      
      //  
      double cmdar = 1.0/fabs( cos( m_darkAngRad));
      // y is the direction in thickness
      // x is the direction in width
      for(int i=0; i<( m_ntpts+1); i++)
        {
	  
	  m_y[i] = m_dt*(i + 0.5); // 
	  m_li[i] = m_y[i]*cmdar; // length of incident path 
        }
      for(int j=0; j<( m_nwpts+1); j++) m_x[j] = m_dw*(j + 0.5);
      for(int i=0; i<( m_ntpts+1); i++)
        {
	  for(int j=0; j<( m_nwpts+1); j++)
            {
	      
	      double a = atan( m_y[i]/m_x[j]);
	      double b = atan( (m_th - m_y[i])/m_x[j]);
	      
	      int idx = i*( m_nwpts+1) + j;
	      m_th1[idx] = m_darkAngRad - b;
	      m_th2[idx] = m_darkAngRad + a; 
#ifdef DEEPDEBUG
	      std::cout << "x,y = " << m_x[j] << "," <<  m_y[i] << std::endl;
	      std::cout << "th1, th2 = " << m_th1[idx] << "," << m_th2[idx] << std::endl;
#endif
            }
        }
      return;
    } // VanPlateAbsorp::VanPlateAbsorp
    
  } // Reduction::
} // DANSE::

// version
// $Id: VanPlateAbsorp.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
