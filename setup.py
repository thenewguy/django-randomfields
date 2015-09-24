from setuptools import setup, find_packages
from setuptools.command.test import test as SetuptoolsTestCommand
from sys import version_info

class RunTestsCommand(SetuptoolsTestCommand):
    def initialize_options(self):
        SetuptoolsTestCommand.initialize_options(self)
        self.test_suite = "override"

    def finalize_options(self):
        SetuptoolsTestCommand.finalize_options(self)
        self.test_suite = None

    def run(self):
        SetuptoolsTestCommand.run(self)
        self.with_project_on_sys_path(self.run_tests)

    def run_tests(self):
        import coverage.cmdline
        import os
        
        owd = os.path.abspath(os.getcwd())
        nwd = os.path.abspath(os.path.dirname(__file__))
        os.chdir(nwd)
        
        errno = coverage.cmdline.main(['run', os.path.abspath('test_project/manage.py'), 'test', nwd, os.path.abspath('test_project')])
        coverage.cmdline.main(['report', '-m'])
        
        os.chdir(owd)
        
        raise SystemExit(errno)

tests_require = ['coverage', 'beautifulsoup4', 'html5lib']
if version_info < (3, 3):
    tests_require = tests_require + ['mock', 'pbr<1.7.0']

setup(
    name = "django-randomfields",
    version = "0.0.1",
    description = "Random fields for django models",
    cmdclass={'test': RunTestsCommand},
    packages=find_packages(),
    install_requires=['django'],
    tests_require=tests_require,
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
