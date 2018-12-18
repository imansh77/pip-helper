from main import OpenFiles, ModuleOrLibrary, UsedImported, GetModulesAndLibrariesNames, SeparationWithBuiltin
import unittest

f = SeparationWithBuiltin()
c = f.used_installed_packages()
print(c)
