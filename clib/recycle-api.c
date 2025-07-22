#include <windows.h>
#include <shlobj.h>
#include <wchar.h>
#include <shellapi.h>
#include <stdio.h>
#include <string.h>
#include <Python.h>

/**
 * This function turns regular char* strings into wchar_t* strings
 * for the use in recycle function.
 */
wchar_t* char_to_wchar(const char* str) {
  if (!str) return NULL;

  int size_needed = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
  if (size_needed <= 0) {
    return NULL;
  }

  wchar_t* wstr = (wchar_t*)malloc(size_needed * sizeof(wchar_t));
  if (!wstr) {
    return NULL;
  }

  int chars_converted = MultiByteToWideChar(CP_UTF8, 0, str, -1, wstr, size_needed);
  if (!chars_converted) {
    free(wstr);
    return NULL;
  }

  return(wstr);
}

/**
 * This function checks the recycle bin status
 * and returns a list containing:
 * [success_flag, num_items, total_size]
 */
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


/**
 * This function sends a file to the recycle bin.
 * It does not check if the file exists; a Python wrapper should ensure existence.
 * @param spath: Path to the file to be recycled.
 * @return: Integer indicating the execution status.
 */
static PyObject* recycle(PyObject* self, PyObject* args) {
  const char* spath;

  if (!PyArg_ParseTuple(args, "s", &spath)) {
    return NULL;
  }
  
  size_t len = strlen(spath);
  char* safe_spath = (char*)malloc(len + 1);
  if (!safe_spath) {
    return NULL;
  }
  memcpy(safe_spath, spath, len);
  safe_spath[len] = '\0';


  wchar_t* path = char_to_wchar(safe_spath);
  free(safe_spath);
  if (!path) {
    return NULL;
  }

  SHFILEOPSTRUCTW fileOp = {0};

  wchar_t from[MAX_PATH + 1];
  wcsncpy(from, path, MAX_PATH);
  from[MAX_PATH] = L'\0';
  from[wcslen(from) + 1] = L'\0';

  fileOp.wFunc = FO_DELETE;
  fileOp.pFrom = from;
  fileOp.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT;

  int result = SHFileOperationW(&fileOp);
  free(path);
  return PyLong_FromLong(result);

}

static PyMethodDef RecycleMethods[] = {
    {"check_recycle_bin", (PyCFunction)check_recycle_bin, METH_NOARGS, "Check the recycle bin status."},
    {"recycle", (PyCFunction)recycle, METH_VARARGS, "Send a file to the recycle bin."},
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
