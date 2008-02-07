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


#ifndef H_ARCSEVENTDATA_EVENT
#define H_ARCSEVENTDATA_EVENT

namespace ARCS_EventData{

  /// @brief Event struct of SNS pre-Nexus event mode data file
  /// Event mode data files are raw binary files. Every 8 bytes 
  /// of the event -mode data file forms an event.
  /// The first 4 bytes is tof (100us). And the last 4 bytes is pixelID.
  /// All event-mode data files are created in windows machines, 
  /// so they are little-endian; you need to convert data files
  /// in big-endian machines like PowerPC-based Mac.
  struct Event {
    unsigned int tof;
    unsigned int pixelID;
  };

}


#endif // H_ARCSEVENTDATA_EVENT


// version
// $Id$

// End of file 
