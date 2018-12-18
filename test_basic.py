import unittest
from main import *
import config


class TestPathHelper(unittest.TestCase, PathHelper):

	def setUp(self):
		self.path = '/Coding/GitHub/todo'
		self.config_path = config.project_path
		self.config_venv_path = config.project_virtualenv_path

	def test_project_path(self):
		self.assertEqual(PathHelper.project_path(self), self.config_path)

	def test_project_virtualenv_path(self):
		self.assertEqual(PathHelper.project_virtualenv_path(self), self.config_venv_path)

	def test_both_path(self):
		self.assertEqual(PathHelper.both_path(self, which_path=self.config_path), self.config_path)
		self.assertEqual(PathHelper.both_path(self, which_path=self.config_venv_path), self.config_venv_path)

	def test_path_is_valid(self):
		self.assertTrue(PathHelper.path_is_valid(self.path))

	def test_path_returner(self):
		self.assertEqual(PathHelper.path_returner(self, which_path=config.project_path), self.config_path)

	def test_if_any_py_files(self):
		self.assertTrue(PathHelper.if_any_py_file)


if __name__ == '__main__':
	unittest.main()
