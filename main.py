from cli import CliHelper
import os
from contextlib import closing


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

	def has_import(self):
		unique_lines = set()
		for line in self.open_files():
			if 'import ' in line:
				unique_lines.add(line.replace('\n', '').replace('\t', ''))
			else:
				print("no imported library found")
		print(unique_lines)
