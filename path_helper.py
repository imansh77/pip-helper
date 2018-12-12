import config

import os
import sys


class PathHelper:
	"""Gets the path of project """

	def __init__(self):
		self.path = None

	def path_getter(self):
		if len(config.project_path) > 0:
			self.path = config.project_path
			return self.path
		else:
			sys.exit("please enter a path")

	def path_is_valid(self):
		if os.path.exists(self.path_getter()):
			return self.path_getter()
		else:
			sys.exit("invalid path")

	def if_any_py_file(self):
		py_files = 0
		for i in os.listdir(self.path_is_valid()):
			if i.endswith(".py"):
				py_files += 1
				break
		if py_files > 0:
			return True
		else:
			sys.exit("There is no py file in this path")
