import os
import sys


class CliHelper:
	"""Gets the path of project """

	def __init__(self):
		self.path = None

	def path_getter(self):
		try:
			self.path = sys.argv[1]
		except Exception:
			sys.exit("please enter a path")

		return self.path

	def path_is_valid(self):
		if os.path.exists(self.path_getter()):
			return True
		else:
			sys.exit("invalid path")
