#include <windows.h>
#include <shlobj.h>
#include <wchar.h>
#include <shellapi.h>
#include <Python.h>

static PyObject* check_recycle_bin() {
  SHQUERYRBINFO info;
  info.cbSize = sizeof(SHQUERYRBINFO);

  HRESULT hr = SHQueryRecycleBin(NULL, &info);
  PyObject* result = PyList_New(0);
  if (SUCCEEDED(hr)) {
    PyObject* suflag = PyBool_FromLong((long)1);
    PyList_Append(result, suflag);
    PyList_Append(result, PyLong_FromUnsignedLongLong(info.i64NumItems));
    PyList_Append(result, PyLong_FromUnsignedLongLong(info.i64Size));
  } else {
    PyObject* suflag = PyBool_FromLong((long)0);
    PyList_Append(result, suflag);
    wprintf(L"Failed to query recycle bin. HRESULT: 0x%08X\n", hr);
  }

  return result;
}

static PyMethodDef RecycleMethods[] = {
    {"check_recycle_bin", (PyCFunction)check_recycle_bin, METH_NOARGS, "Check the recycle bin status."},
    {NULL, NULL, 0, NULL}  // Sentinel
};

static struct PyModuleDef recyclemodule = {
    PyModuleDef_HEAD_INIT,
    "recycle_api",
    NULL,
    -1,
    RecycleMethods
};

PyMODINIT_FUNC PyInit_recycle_api(void) {
  return PyModule_Create(&recyclemodule);
}

int main() {

  printf("Hello World\n");

  return 0;
}
