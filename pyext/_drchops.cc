// -*- C++ -*-
//
// Jiao Lin <jiao.lin@gmail.com>
//

#include <portinfo>

#include <Python.h>

#if PY_MAJOR_VERSION >= 3
#define MOD_ERROR_VAL NULL
#define MOD_SUCCESS_VAL(val) val
#define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
#define MOD_DEF(ob, name, doc, methods)                                 \
  static struct PyModuleDef moduledef = {                               \
                                         PyModuleDef_HEAD_INIT, name, doc, -1, methods, }; \
  ob = PyModule_Create(&moduledef);
#else
#define MOD_ERROR_VAL
#define MOD_SUCCESS_VAL(val)
#define MOD_INIT(name) void init##name(void)
#define MOD_DEF(ob, name, doc, methods)         \
  ob = Py_InitModule3(name, methods, doc);
#endif

//numpy stuff
#define PY_ARRAY_UNIQUE_SYMBOL reduction_ARRAY_API
#include "numpy/arrayobject.h"


#include "exceptions.h"
#include "bindings.h"


char pydrchops_module__doc__[] = "";

// Initialization function for the module (*must* be called initdrchops)
extern "C"
MOD_INIT(_drchops)
{
    // create the module and add the functions
    PyObject * m;
    MOD_DEF(m, "_drchops", pydrchops_module__doc__, pydrchops_methods)

    if (m == NULL)
      return MOD_ERROR_VAL;

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

    return MOD_SUCCESS_VAL(m);
}

// End of file
