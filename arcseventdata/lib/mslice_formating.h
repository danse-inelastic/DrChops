#ifndef H_ARCS_EVENTDATA_MSLICE_FORMATING
#define H_ARCS_EVENTDATA_MSLICE_FORMATING


namespace ARCS_EventData {

  template <typename Iterator>
  const char * SGrid_str
  ( const Iterator Spe, const Iterator SEpe,
    size_t ntotpixels, size_t nEbins);
  
}


#include "mslice_formating.icc"

#endif// H_ARCS_EVENTDATA_MSLICE_FORMATING
