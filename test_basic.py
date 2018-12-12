from main import OpenFiles, ModuleOrLibrary, UsedImported, GetModulesAndLibrariesNames, TxtFile
import unittest

f = OpenFiles()
c = f.if_any_py_file()
print(c)
