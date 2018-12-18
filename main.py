from path_helper import PathHelper

import os
import sys
import itertools


class OpenFiles(PathHelper):

	def py_files(self):
		if self.if_any_py_file():
			for dirpath, dirnames, filenames in os.walk(self.path_returner(self.project_path())):
				for filename in [i for i in filenames if i.endswith(".py")]:
					yield(os.path.join(dirpath, filename))

	def opened_files(self):
		for file in self.py_files():
			with open(file, 'r') as opened_file:
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
			if every_import in os.listdir(self.path_returner(self.project_path())):
				modules_name.append(every_import.replace('.py', ''))
			else:
				libraries_name.append(every_import.replace('.py', ''))
		return [modules_name, libraries_name]


class UsedImported(ModuleOrLibrary, OpenFiles):

	def which_lib_is_used(self):
		return self.lib_or_module(i=1)

	def which_module_is_used(self):
		return self.lib_or_module(i=0)

	def lib_or_module(self, i):
		all_libs_or_modules = self.check_if_module_or_library()[i]
		before = self.module_and_lib_set()[2]
		after = self.module_and_lib_set()[1]
		used_ones = set([i for line in self.opened_files() for i in all_libs_or_modules if i+'.' in line])
		for line in self.opened_files():
			for after_import in after:
				if after_import + '.' in line and "#" not in line:
					if before[after.index(after_import)] in all_libs_or_modules:
						used_ones.add(before[after.index(after_import)])
		return used_ones


class SeparationWithBuiltin(UsedImported):

	def installed_packages(self):
		return os.listdir(self.path_returner(self.project_virtualenv_path()))

	def used_installed_packages(self):
		installed_packs = [i for i in self.which_lib_is_used() if i in self.installed_packages()]
		return installed_packs


class TxtFile(SeparationWithBuiltin):

	def requirements_maker(self):
		with open('requirements.txt', 'w') as file:
			for used_installed in self.used_installed_packages():
				file.write(used_installed+'\n')


TxtFile().requirements_maker()
