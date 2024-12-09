# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:17:15 2024

@author: mbmad
"""

from setuptools import setup, find_packages
import os

# Read metadata from the metadata file
metadata = {}
with open(os.path.join("autosleap", "__init__.py")) as f:
    exec(f.read(), metadata)

setup(
    name='autosleap',
    version=metadata['__version__'],  # Dynamically fetch version
    description='A mini application for automatic SLEAP analysis',
    author='Maxwell Madden',
    author_email='mxwllmadden@gmail.com',
    url='https://github.com/mxwllmadden/autosleap',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'numpy',
        'Pillow'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'autosleap=autosleap.cli_parser:main',  # Replace with your entry point
        ],
    },
)
