// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               T. M. Kelley
//                        California Institute of Technology
//                        (C) 1998-2004  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "misc.h"


// copyright

char pyreduction_copyright__doc__[] = "";
char pyreduction_copyright__name__[] = "copyright";

static char pyreduction_copyright_note[] = 
  "reduction python module: Copyright (c) 1998-2005 T. M. Kelley, "
  "Copyright (c) 2005-2007 Jiao Lin.";


PyObject * pyreduction_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pyreduction_copyright_note);
}
    
    
// version
// $Id: misc.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
