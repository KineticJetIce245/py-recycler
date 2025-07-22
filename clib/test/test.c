#include <windows.h>
#include <shlobj.h>
#include <wchar.h>
#include <shellapi.h>
#include <stdio.h>
#include <string.h>

int recycle(const wchar_t* path) {
  SHFILEOPSTRUCTW fileOp = {0};

  wchar_t from[MAX_PATH + 1];
  wcsncpy(from, path, MAX_PATH);
  from[MAX_PATH] = L'\0';
  from[wcslen(from) + 1] = L'\0';

  fileOp.wFunc = FO_DELETE;
  fileOp.pFrom = from;
  fileOp.fFlags = FOF_ALLOWUNDO;// | FOF_NOCONFIRMATION | FOF_SILENT;

  int result = SHFileOperationW(&fileOp);
  return result;
}

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

int main() {
  const char* str = "test.file";
  wchar_t* wide_str = char_to_wchar(str);
  recycle(wide_str);
  return 0;
}
