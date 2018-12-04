from cli import CliHelper
import os, sys
# import sys
from contextlib import closing
import itertools


class OpenFiles(CliHelper):

	def find_py_files(self):
		files_name = []
		if self.path_is_valid():
			for filename in os.listdir(self.path_getter()):
				if filename.endswith(".py"):
					files_name.append(filename)
		return files_name

	def opened_files(self):
		for file in self.find_py_files():
			with open(self.path_getter()+'/'+file, 'r') as opened_file:
				for line in opened_file:
					yield line


class GetModulesAndLibrariesNames(OpenFiles):

	def import_getter(self):
		unique_lines = set()
		for line in self.opened_files():
			try:
				if 'import ' in line:
					unique_lines.add(line.replace('\n', '').replace('\t', ''))
			except:
				sys.exit('there is no library or module imported in this directory')
		return unique_lines

	def module_and_lib_set(self):
		module_and_lib_names = []
		for every_import in self.import_getter():
			if every_import.startswith('import'):
				names_list = every_import.split('import ')[1].split(', ')
				module_and_lib_names.append(names_list)
			elif every_import.startswith('from'):
				names_list = [every_import.split('from ')[1].split()[0]]
				module_and_lib_names.append(names_list)
		convert_to_flat = list(itertools.chain.from_iterable(module_and_lib_names))
		module_and_lib_names = set(convert_to_flat)

		return module_and_lib_names


class ModuleOrLibrary(GetModulesAndLibrariesNames):

	def concat_names(self):
		py_files = [each_name+'.py' for each_name in self.module_and_lib_set()]
		return py_files

	def check_if_module_or_library(self):
		modules_name = []
		libraries_name = []
		for every_import in self.concat_names():
			if every_import in os.listdir(self.path_getter()):
				modules_name.append(every_import.replace('.py', ''))
			else:
				libraries_name.append(every_import.replace('.py', ''))

		return [modules_name, libraries_name]


class UsedImported(ModuleOrLibrary, OpenFiles):

	def which_lib_is_used(self):
		used_libs = set()
		all_libs = self.check_if_module_or_library()[1]
		for lib in all_libs:
			for file in self.opened_files():
				if str(lib+'.') in file:
					used_libs.add(lib)
		return used_libs
