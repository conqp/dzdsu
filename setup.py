#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name='dzdsu',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    python_requires='>=3.10',
    packages=['dzdsu'],
    entry_points={
        'console_scripts': [
            'dzdsu = dzdsu.utility:main',
            'dzdsw = dzdsu.wrapper:main'
        ]
    },
    url='https://github.com/conqp/dzdsu',
    license='GPLv3',
    description='DayZ dedicated server utilities',
    keywords='DayZ dedicated server utilities'
)
