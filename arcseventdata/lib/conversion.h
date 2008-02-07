#ifndef H_ARCS_EVENTDATA_CONVERSION
#define H_ARCS_EVENTDATA_CONVERSION


namespace ARCS_EventData {
  
  const double pi = 3.1415926535897;

  const double V2K = 1.58801E-3; // Convert v[m/s] to k[1/AA]
  const double K2V = 1./V2K; // Convert k[1/AA] to v[m/s] 
  const double SE2V = 437.3949;  /* Convert sqrt(E)[meV] to v[m/s] */
  const double VS2E = 5.227e-6;	 /* Convert (v[m/s])**2 to E[meV] */

}


#endif// H_ARCS_EVENTDATA_CONVERSION
