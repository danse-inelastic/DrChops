// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "misc.h"


// copyright

char pydrchops_copyright__doc__[] = "";
char pydrchops_copyright__name__[] = "copyright";

static char pydrchops_copyright_note[] = 
    "drchops python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pydrchops_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pydrchops_copyright_note);
}
    
    
// version
// $Id$

// End of file
