from distutils.core import setup

setup(
    name = "django-randomfields",
    version = "0.0.1",
    description = "Random fields for django models",
    package_dir = {'': 'project'},
    packages = [
        "randomfields",
        "randomfields.fields",
    ],
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
