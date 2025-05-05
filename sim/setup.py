# setup.py
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import setuptools

# Pybind11-specific build extension - based on pybind11 documentation
class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked.
    """
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

# As of Python 3.