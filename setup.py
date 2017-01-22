import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mailadmin',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'django >= 1.10, < 2.0'
    ],
    include_package_data=True,
    license='BSD-3-Clause',
    description='Web-based email administration software.',
    long_description=README,
    url='https://www.kapp-hamburg.de/mailadmin/',
    author='Thorben Nissen',
    author_email='thorben.nissen@kapp-hamburg.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Email',
    ],
)
