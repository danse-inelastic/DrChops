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

#include "exceptions.h"
#include "bindings.h"


//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL reduction_ARRAY_API
#include "numpy/arrayobject.h"


char pyreduction_module__doc__[] = "";

// Initialization function for the module (*must* be called initreduction)
extern "C"
void
initreduction()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "reduction", pyreduction_methods,
        pyreduction_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module reduction");
    }

    // install the module exceptions
    pyreduction_runtimeError = PyErr_NewException("reduction.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pyreduction_runtimeError);

    // numpy
    import_array();

    return;
}

// version
// $Id: reductionmodule.cc 1306 2007-07-13 14:07:32Z linjiao $

// End of file
