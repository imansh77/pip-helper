import unittest
from main import *
import config


class TestPathHelper(unittest.TestCase, TxtFile):

	def setUp(self):
		self.path = '/Coding/GitHub/todo'
		self.test_for_expected_output = '/Coding/GitHub/pip-helper/pip-helper/path_helper.py'
		self.line_example = 'TxtFile().requirements_maker()\n'
		self.used_libs = {'sys', 'unittest', 'itertools', 'os', 'logging'}
		self.used_mods = {'path_helper', 'config'}
		self.example_used_installed_packages = []
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

	def test_py_files(self):
		self.assertIn(self.test_for_expected_output, list(self.py_files()))

	def test_opened_files(self):
		self.assertIn(self.line_example, list(self.opened_files()))

	def test_import_getter(self):
		for i in self.import_getter():
			if 'import ' not in i:
				self.assertIn('import ', i)

	def test_module_and_lib_set(self):
		self.assertIn('os', list(self.module_and_lib_set()[0]))
		self.assertIn('PathHelper', list(self.module_and_lib_set()[1]))
		self.assertIn('path_helper', list(self.module_and_lib_set()[2]))

	def test_concat_names(self):
		self.assertIn('.py', str(list(self.py_files())))

	def test_check_if_module_or_library(self):
		self.assertIn('config', self.check_if_module_or_library()[0])
		self.assertNotIn('unittest', self.check_if_module_or_library()[0])
		self.assertIn('unittest', self.check_if_module_or_library()[1])
		self.assertNotIn('config', self.check_if_module_or_library()[1])

	def test_which_lib_is_used(self):
		self.assertEqual(self.used_libs, self.which_lib_is_used())

	def test_which_module_is_used(self):
		self.assertEqual(self.used_mods, self.which_module_is_used())

	def test_lib_or_module(self):
		self.assertEqual(self.used_mods, self.lib_or_module(i=0)[0])
		self.assertEqual(self.used_libs, self.lib_or_module(i=1)[0])

	def test_installed_packages(self):
		self.assertIn('requests', self.installed_packages())

	def test_used_installed_packages(self):
		self.assertEqual(self.example_used_installed_packages, self.used_installed_packages())


if __name__ == '__main__':
	unittest.main()
