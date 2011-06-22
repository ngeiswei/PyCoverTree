#!/usr/bin/env python
from distutils.core import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PyCoverTree",
    version = "0.1",
    author = "Thomas Kollar",
    author_email = "tkollar@csail.mit.edu",
    description = ("Python library of cover tree (http://hunch.net/~jl/projects/cover_tree/cover_tree.html) for fast nearest neighbor querying."),
    license = "BSD",
    keywords = "cover tree nearest neighbor",
    url = "https://github.com/ngeiswei/PyCoverTree",
    packages=['covertree'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    # entry_points="""[my.plugins] myFoo = covertree:CoverTree"""
)
