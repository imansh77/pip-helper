from cli import CliHelper
import os, sys
# import sys
from contextlib import closing
import itertools


class OpenFiles:
	input = CliHelper()

	def find_py_files(self):
		files_name = []
		if self.input.path_is_valid():
			for filename in os.listdir(self.input.path_getter()):
				if filename.endswith(".py"):
					files_name.append(filename)
		return files_name

	def open_files(self):
		py_files_list = self.find_py_files()
		for file in py_files_list:
			with open(file, 'r') as fin:
				for line in fin:
					yield line


class ModuleOrLibrary(OpenFiles):

	def import_getter(self):
		unique_lines = set()
		for line in self.open_files():
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
