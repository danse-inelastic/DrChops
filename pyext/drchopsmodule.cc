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

//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL reduction_ARRAY_API
#include "numpy/arrayobject.h"


#include "exceptions.h"
#include "bindings.h"


char pydrchops_module__doc__[] = "";

// Initialization function for the module (*must* be called initdrchops)
extern "C"
void
initdrchops()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "drchops", pydrchops_methods,
        pydrchops_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module drchops");
    }

    // install the module exceptions
    pydrchops_runtimeError = PyErr_NewException("drchops.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pydrchops_runtimeError);

    // numpy
    import_array();

    return;
}

// version
// $Id$

// End of file
