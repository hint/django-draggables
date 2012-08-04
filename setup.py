#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import draggables


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: JavaScript',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: User Interfaces',
]

setup(
    author='Piotr Kilczuk',
    author_email='piotr@tymaszweb.pl',
    name='django-draggables',
    version=draggables.__version__,
    description='New generation drag&drop for Django admin',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/TyMaszWeb/django-draggables',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2',
        'django-admin-jqueryui>=1.8.11',
    ],
    tests_require=[
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,
    #test_suite = 'runtests.main',
)
