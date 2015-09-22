from setuptools import setup, find_packages
from setuptools.command.test import test as SetuptoolsTestCommand

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
        
        errno = coverage.cmdline.main(['run', os.path.abspath('test_project/manage.py'), 'test'])
        coverage.cmdline.main(['report', '-m'])
        
        os.chdir(owd)
        
        raise SystemExit(errno)

setup(
    name = "django-randomfields",
    version = "0.0.1",
    description = "Random fields for django models",
    cmdclass={'test': RunTestsCommand},
    packages=find_packages('.'),
    install_requires=['django'],
    tests_require=['coverage'],
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
