from cli import CliHelper
import os
import sys
from contextlib import closing
import contextlib
import itertools
import re


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
		after_import = []
		before_import = []
		for every_import in self.import_getter():
			if every_import.startswith('import'):
				names_list = every_import.split('import ')[1].split(', ')
				module_and_lib_names.append(names_list)
			elif every_import.startswith('from'):
				names_list = [every_import.split('from ')[1].split('import')[0].strip()]
				after_import_list = [every_import.split('from ')[1].split('import')[1].strip().strip(',')]
				for i in after_import_list:
					after_import.append(i)
				for i in names_list:
					before_import.append(i)
				module_and_lib_names.append(names_list)
		convert_to_flat = list(itertools.chain.from_iterable(module_and_lib_names))
		module_and_lib_names = set(convert_to_flat)
		return module_and_lib_names, after_import, before_import


class ModuleOrLibrary(GetModulesAndLibrariesNames):

	def concat_names(self):
		py_files = [each_name+'.py' for each_name in self.module_and_lib_set()[0]]
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

	def lib_or_module(self, i):
		all_libs_or_modules = self.check_if_module_or_library()[i]
		before = self.module_and_lib_set()[2]
		after = self.module_and_lib_set()[1]
		used_ones = set([i for line in self.opened_files() for i in all_libs_or_modules if i+'.' in line])
		print(before)
		print(after)

		for line in self.opened_files():
			for j in after:
				if (j + '.') in line and not "#" in line:
					print(after.index(j))
					used_ones.add(before[after.index(j)])
		return used_ones

	def which_lib_is_used(self):
		return self.lib_or_module(i=1)

	def which_module_is_used(self):
		return self.lib_or_module(i=0)

	def clo(self):
		return CliHelper.mro
