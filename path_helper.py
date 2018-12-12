import config

import os
import sys


class PathHelper:
	"""Gets the path of project """

	def __init__(self):
		self.path = None

	def project_path(self):
		return self.both_path(which_path=config.project_path)

	def project_virtualenv_path(self):
		return self.both_path(which_path=config.project_virtualenv_path)

	def both_path(self, which_path):
		if (len(which_path)) > 0:
			self.path = which_path
			return self.path
		else:
			sys.exit("please provide both project_path & project_virtualenv_path in config.py")

	@staticmethod
	def path_is_valid(which_path):
		if os.path.exists(which_path):
			return True
		else:
			sys.exit("invalid path")

	def path_returner(self, which_path):
		if self.path_is_valid(which_path=which_path):
			return which_path

	def if_any_py_file(self):
		py_files = 0
		for i in os.listdir(self.path_returner(self.project_path())):
			if i.endswith(".py"):
				py_files += 1
				break
		if py_files > 0:
			return True
		else:
			sys.exit("There is no py file in this path")
