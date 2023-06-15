#include "Python.h"
#include <math.h>

void rotate2d_(double pos0, double pos1, double rad, double *p0, double *p1) {
    double s, c;
    s = sin(rad);
    c = cos(rad);
    *p0 = pos0 * c - pos1 * s;
    *p1 = pos1 * c + pos0 * s;
}

static PyObject* rotate2d(PyObject* self, PyObject* args) {
    double pos0, pos1, rad, p0, p1, s, c;
    if (!PyArg_ParseTuple(args, "ddd", &pos0, &pos1, &rad))
        return NULL;

    rotate2d_(pos0, pos1, rad, &p0, &p1);
    return Py_BuildValue("dd", p0, p1);
}

static PyObject* f_viewcoordinate(PyObject* self, PyObject* args) {
    double position1, position2, position3, vertex1, vertex2, vertex3, rot1, rot2, x, y, z;
    if (!PyArg_ParseTuple(args, "dddddddd", &position1, &position2, &position3, &vertex1, &vertex2, &vertex3, &rot1, &rot2))
        return NULL;

    x = vertex1 - position1;
    y = vertex2 - position2;
    z = vertex3 - position3;

    rotate2d_(x, z, rot2, &x, &z);
    rotate2d_(y, z, rot1, &y, &z);

    return Py_BuildValue("ddd", x, y, z);
}


// # def f_viewcoordinate(position1, position2, position3, vertex1, vertex2, vertex3, rot1, rot2):
// #     x = vertex1 - position1
// #     y = vertex2 - position2
// #     z = vertex3 - position3
// #     x, z = rotate2d(x, z, rot2)
// #     y, z = rotate2d(y, z, rot1)
// #     return x, y, z

static PyMethodDef mainMethods[] = {
    {
        "rotate2d",
        rotate2d,
        METH_VARARGS,
        "Rotate 2d"
    },
    {
        "f_viewcoordinate",
        f_viewcoordinate,
        METH_VARARGS,
        "viewcoordinate"
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};

static PyModuleDef pytouch_c = {
    PyModuleDef_HEAD_INIT,
    "pytouch_c",
    "pytouch functions",
    -1,
    mainMethods
};

PyMODINIT_FUNC PyInit_pytouch_c(void) {
    return PyModule_Create(&pytouch_c);
}