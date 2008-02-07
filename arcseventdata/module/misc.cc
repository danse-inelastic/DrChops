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
//#include "libarcseventdata/hello.h"


// copyright

char pyarcseventdata_copyright__doc__[] = "";
char pyarcseventdata_copyright__name__[] = "copyright";

static char pyarcseventdata_copyright_note[] = 
    "arcseventdata python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pyarcseventdata_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pyarcseventdata_copyright_note);
}
    
// hello

char pyarcseventdata_hello__doc__[] = "";
char pyarcseventdata_hello__name__[] = "hello";

PyObject * pyarcseventdata_hello(PyObject *, PyObject *)
{
    return Py_BuildValue("s", "hello");
}
    
// version
// $Id$

// End of file
